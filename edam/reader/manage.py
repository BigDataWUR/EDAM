import logging
from io import StringIO

import pandas as pd
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import Query
from sqlalchemy.orm import scoped_session, sessionmaker

from edam.reader.models.AbstractObservable import AbstractObservable
from edam.reader.models.Sensor import Sensor
from edam.reader.models.Station import Station
from edam.reader.models.UnitOfMeasurement import UnitOfMeasurement

from edam.settings import database_url, database_type

module_logger = logging.getLogger('edam.reader.manage')


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    module_logger.debug(
        f'Received a call to `db_connect()`. Database url is: {database_url}')
    return create_engine(database_url)


engine = db_connect()

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


class DatabaseHandler(object):
    """
    This class handles database operations (add item, add dataframes, etc.)
    """

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        """
        self.db_handler_logger = logging.getLogger(
            'edam.reader.manage.DatabaseHandler')

        self.engine = engine

        self.Session = db_session

    def clean_df_db_dups(self, df, tablename, dup_cols=None,
                         filter_continuous_col=None, filter_categorical_col=None):
        """
        code https://github.com/ryanbaumann/Pandas-to_sql-upsert/blob/master/to_sql_newrows.py
        Remove rows from a dataframe that already exist in a database

        :type df: pandas.DataFrame
        :type dup_cols: list
        :param df: dataframe to remove duplicate rows from
        :param tablename: tablename to check duplicates in
        :param dup_cols: list or tuple of column names to \
        check for duplicate row values
        :param filter_continuous_col: the name of the continuous \
        data column for BETWEEEN min/max filter can be either\
        a datetime, int, or float data type useful for restricting \
        the database table size to check
        :param filter_categorical_col: the name of the categorical \
        data column for Where = value check \
        Creates an "IN ()" check on the unique values in this column
        :return: Unique list of values from dataframe compared to database table

        """
        if dup_cols is None:
            dup_cols = []
        engine = self.engine
        args = 'SELECT {} FROM {}'.format(', '.join(['"{0}"'.format(col) for col in dup_cols]), tablename)
        args_contin_filter, args_cat_filter = None, None
        if filter_continuous_col is not None:
            if df[filter_continuous_col].dtype == 'datetime64[ns]':
                args_contin_filter = f""" "{filter_continuous_col}" BETWEEN Convert(datetime, '{df[filter_continuous_col].min()}')
                                              AND Convert(datetime, '{df[filter_continuous_col].max()}')"""

        if filter_categorical_col is not None:
            args_cat_filter = ' "{}" in({})'.format(filter_categorical_col,
                                                    ', '.join(["'{0}'".format(value) for value in
                                                               df[filter_categorical_col].unique()]))

        if args_contin_filter and args_cat_filter:
            args += ' Where ' + args_contin_filter + ' AND' + args_cat_filter
        elif args_contin_filter:
            args += ' Where ' + args_contin_filter
        elif args_cat_filter:
            args += ' Where ' + args_cat_filter

        df.drop_duplicates(dup_cols, keep='last', inplace=True)
        df2 = pd.read_sql(args, engine)
        for column in list(df):
            if df[column].dtype == "float64":
                df[column] = df[column].astype(str)
                df2[column] = df2[column].astype(str)

        df = pd.merge(df, df2, how='left', on=dup_cols, indicator=True)

        df = df[df['_merge'] == 'left_only']
        df.drop(['_merge'], axis=1, inplace=True)
        if "tation" in tablename:
            if database_type == "postgresql":
                df['id'] = pd.read_sql_query('select coalesce(max(id),0)+1 from public.\"Station\"',
                                             engine).iloc[0, 0] + range(len(df))
            elif database_type == "sqlite":
                df['id'] = \
                    pd.read_sql_query('select coalesce(max(id),0)+1 from Station', engine).iloc[
                        0, 0] + range(len(df))
            df.set_index(['id'], inplace=True)

        return df

    @staticmethod
    def __add_dataframe__(dataframe: pd.DataFrame, table='Observations', index=True,
                          index_label='timestamp'):
        engine = create_engine(database_url)

        def create_file_object(
                df, file_path=None, string_io=True, index=index):
            """Creates a csv file or writes to memory"""
            if string_io:
                s_buf = StringIO()
                df.to_csv(s_buf, date_format="%Y-%m-%d %H:%M:%S", index=index)
                s_buf.seek(0)
                file_object = s_buf
            else:
                df.to_csv(file_path, index=False)
                df = open(file_path)
                file_object = df
            return file_object

        def load_to_database(table1, unique_columns, file_object):

            connection = engine.raw_connection()
            try:
                cursor = connection.cursor()

                columns = ', '.join(['{}'.format(col) for col in unique_columns])
                sql = f'COPY "{table1}" ({columns}) FROM STDIN WITH CSV HEADER'
                cursor.copy_expert(sql=sql, file=file_object)

                connection.commit()

                connection.close()
            finally:
                pass

        if database_type == "postgresql":
            df_index_name = dataframe.index.name
            if df_index_name == "id" or df_index_name is None:
                unique_columns = list(dataframe)
                index = False
            else:
                unique_columns = list()
                unique_columns.append(df_index_name)
                unique_columns += list(dataframe)
                index = True
            load_to_database(
                table,
                unique_columns,
                create_file_object(
                    dataframe,
                    index=index))
        elif database_type == "sqlite":
            dataframe.to_sql(name=table, con=engine, if_exists='append',
                             index=index, index_label=index_label)

    def __add_item__(self, item):
        """

        :param item:
        :return: True, item.id
        """
        session = self.Session()
        session.expire_on_commit = False
        try:
            session.add(item)
            session.commit()
        except BaseException:
            self.db_handler_logger.error(
                'Exception when adding %s. Check __add_item__()' %
                item)
            session.rollback()
            raise
        finally:
            session.flush()
        session.close()
        return True, item.id

    def __update_item__(self, item, metadata_dict):
        session = self.Session()
        returned_item = session.query(item.__class__).filter(
            item.__class__.id == item.id).first()  # type: item.__class__
        returned_item.update_metadata(metadata_dict)
        session.commit()
        session.close()


if __name__ == "__main__":
    pass
