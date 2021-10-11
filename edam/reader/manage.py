import logging
from io import StringIO

import pandas as pd
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import Query
from sqlalchemy.orm import scoped_session, sessionmaker

from edam.reader.models import Sensors, Station, Observations, \
    Base, AbstractObservables, UnitsOfMeasurement, HelperTemplateIDs
from edam.settings import database_url, database_type

module_logger = logging.getLogger('edam.reader.manage')


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    module_logger.debug(f'Received a call to `db_connect()`. Database url is: {database_url}')
    return create_engine(database_url)


db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db_connect()))


def create_tables(engine):
    """"""
    Base.metadata.create_all(engine)


def drop_tables(engine):
    module_logger.debug('Received a call to `drop_tables()`.')
    module_logger.info('Database tables dropped using drop_tables()')
    Base.metadata.drop_all(engine)


class DatabaseInstantiation(object):
    def __init__(self, drop=True):
        """
        Initializes database connection and sessionmaker.
        """
        db_insta_logger = logging.getLogger('edam.reader.manage.DatabaseInstantiation')
        self.engine = db_connect()
        db_insta_logger.debug('Finding database engine connection string')
        if drop:
            db_insta_logger.debug('Calling drop_tables()')
            drop_tables(self.engine)
        db_insta_logger.debug('Creating database')
        create_tables(self.engine)


class DatabaseHandler(object):
    """
    This class handles database operations (add item, add dataframes, etc.)
    """

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        """
        self.db_handler_logger = logging.getLogger('edam.reader.manage.DatabaseHandler')

        self.engine = db_connect()

        self.Session = db_session

    def clean_df_db_dups(self, df, tablename, dup_cols=None, filter_continuous_col=None, filter_categorical_col=None):
        """
        code: https://github.com/ryanbaumann/Pandas-to_sql-upsert/blob/master/to_sql_newrows.py
        Remove rows from a dataframe that already exist in a database
        Required:
            df : dataframe to remove duplicate rows from
            engine: SQLAlchemy engine object
            tablename: tablename to check duplicates in
            dup_cols: list or tuple of column names to check for duplicate row values
        Optional:
            filter_continuous_col: the name of the continuous data column for BETWEEEN min/max filter
                                   can be either a datetime, int, or float data type
                                   useful for restricting the database table size to check
            filter_categorical_col : the name of the categorical data column for Where = value check
                                     Creates an "IN ()" check on the unique values in this column
        Returns
            Unique list of values from dataframe compared to database table
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
                df['id'] = pd.read_sql_query('select coalesce(max(id),0)+1 from public.\"Station\"', engine).iloc[
                               0, 0] + range(len(df))
            elif database_type == "sqlite":
                df['id'] = pd.read_sql_query('select coalesce(max(id),0)+1 from Station', engine).iloc[
                               0, 0] + range(len(df))
            df.set_index(['id'], inplace=True)

        return df

    @staticmethod
    def __add_dataframe__(dataframe: pd.DataFrame, table='Observations', index=True, index_label='timestamp'):
        engine = create_engine(database_url)

        def create_file_object(df, file_path=None, string_io=True, index=index):
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
                uniq_cols = list(dataframe)
                index = False
            else:
                uniq_cols = list()
                uniq_cols.append(df_index_name)
                uniq_cols += list(dataframe)
                index = True
            load_to_database(table, uniq_cols, create_file_object(dataframe, index=index))
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
        except:
            self.db_handler_logger.error(f'Exception when adding {item}. Check __add_item__()')
            session.rollback()
            raise
        finally:
            session.flush()
        session.close()
        return True, item.id

    def __update_item__(self, item, metadata_dict):
        session = self.Session()
        returned_item = session.query(item.__class__).filter(
            item.__class__.id == item.id).first()  # type: HelperTemplateIDs
        returned_item.update_meta(metadata_dict)
        session.commit()
        session.close()

    def __get_observations_by_id_as_df__(self, observable_id):
        """

        :return: A list with all Observations.
        """
        session = self.Session()
        df = pd.DataFrame()
        q = session.query(Observations).filter(Observations.observable_id == observable_id)  # type: Query
        q = q.order_by(Observations.timestamp.asc())
        df = pd.read_sql(sql=q.statement, con=self.engine, index_col='timestamp')
        df.drop('id', axis=1, inplace=True)
        session.rollback()
        session.close()
        return df

    def __check_station_is_in_db__(self, station: Station):
        session = self.Session()

        exists = session.query(Station.id).filter(and_(Station.name == station.name
                                                       , Station.location == station.location
                                                       , Station.mobile == station.mobile)
                                                  )
        session.rollback()
        session.close()
        return exists.scalar() is not None, exists.first()

    def __check_unit_is_in_db__(self, unit: UnitsOfMeasurement):
        session = self.Session()
        exists = session.query(UnitsOfMeasurement.id).filter(and_(UnitsOfMeasurement.name == unit.name
                                                                  , UnitsOfMeasurement.symbol == unit.symbol
                                                                  )
                                                             )
        session.rollback()
        session.close()
        return exists.scalar() is not None, exists.first()

    def __check_observable_is_in_db__(self, observable: AbstractObservables):
        session = self.Session()
        exists = session.query(AbstractObservables.id).filter(and_(AbstractObservables.name == observable.name
                                                                   ,
                                                                   AbstractObservables.ontology == observable.ontology)
                                                              )
        session.rollback()
        session.close()
        return exists.scalar() is not None, exists.first()

    def __chech_helperTemplateID_is_in_db__(self, helperTemplateID: HelperTemplateIDs):
        session = self.Session()
        exists = session.query(HelperTemplateIDs.id). \
            filter(and_(HelperTemplateIDs.observable_id == helperTemplateID.observable_id,
                        HelperTemplateIDs.unit_id == helperTemplateID.unit_id,
                        HelperTemplateIDs.station_id == helperTemplateID.station_id,
                        HelperTemplateIDs.abstract_observable_id == helperTemplateID.abstract_observable_id,
                        HelperTemplateIDs.sensor_id == helperTemplateID.sensor_id))
        session.rollback()
        session.close()
        return exists.scalar() is not None, exists.first()

    def __check_sensor_is_in_db__(self, sensor: Sensors):
        session = self.Session()
        # TODO: Fix the filter parameters. Needs to be more generic
        # TODO: Implement tags equality check (json error)
        exists = session.query(Sensors.id).filter(and_(Sensors.generic == sensor.generic
                                                       , Sensors.abstract_observable_id == sensor.abstract_observable_id
                                                       , Sensors.manufacturer == sensor.manufacturer
                                                       , Sensors.name == sensor.name
                                                       ))
        session.rollback()
        session.close()
        return exists.scalar() is not None, exists.first()

    def __get_helper_table_row_input_file_observable_id__(self, observable_id,
                                                          station_id) -> HelperTemplateIDs:
        """
        
        :param observable_id: This is usually a short of the Observables name, which is used in templates
         E.g. temp is used for Temperature.
        :return:
        """
        session = self.Session()
        q = session.query(HelperTemplateIDs).filter(and_(HelperTemplateIDs.station_id == station_id,
                                                         HelperTemplateIDs.observable_id == observable_id
                                                         )).first()  # type: HelperTemplateIDs
        session.expunge(q)
        # session.rollback()
        session.close()
        return q

    def __get_observable_by__id__(self, id) -> AbstractObservables:
        """

        :param id: This is the id of the stored Observable
         E.g. 1
        :return:
        """
        session = self.Session()

        q = session.query(AbstractObservables).filter(AbstractObservables.id == id)  # type: Query
        session.rollback()
        session.close()
        return q.first()

    def __update_helper_observable_ids_with_unit_id__(self, station_id, observable_observable_id, unit_id):
        # TODO: This should be more generic
        session = self.Session()

        result = session.query(HelperTemplateIDs).filter(and_(HelperTemplateIDs.station_id == station_id,
                                                              HelperTemplateIDs.observable_id == observable_observable_id
                                                              )).first()  # type: HelperTemplateIDs
        # Above query MUST return one result
        # We update this one
        result.unit_id = unit_id

        session.commit()
        session.close()

    def __update_helper_observable_ids_with_sensor_id__(self, station_id, observable_observable_id,
                                                        sensor_id):
        # TODO: This should be more generic
        session = self.Session()

        result = session.query(HelperTemplateIDs).filter(and_(HelperTemplateIDs.station_id == station_id,
                                                              HelperTemplateIDs.observable_id == observable_observable_id
                                                              )).first()  # type: HelperTemplateIDs
        # Above query MUST return one result
        # We update this one
        result.sensor_id = sensor_id

        session.commit()
        session.close()

    def __get_abstract_observable_id_from_observable_id__(self, station_id, observable_observable_id):
        session = self.Session()
        result = session.query(HelperTemplateIDs).filter(and_(HelperTemplateIDs.station_id == station_id,
                                                              HelperTemplateIDs.observable_id == observable_observable_id
                                                              )).first()  # type: HelperTemplateIDs
        session.expunge_all()
        session.close()
        return result.abstract_observable_id or None

    def __get_station_id_by_tags_station_id__(self, tags_station_id):
        session = self.Session()
        string_to_find = "\"station_id\":\"%d\"" % tags_station_id
        exists = session.query(Station.id).filter(Station.tags.contains(string_to_find))

        if exists.first() is not None:
            database_station_id = exists.first().id
        else:
            database_station_id = None
        session.close()
        return database_station_id

    def get_all_observables(self):
        session = self.Session()
        session.close()
        return session.query(AbstractObservables).all()

    def get_all_stations(self):
        session = self.Session()
        session.close()
        return session.query(Station).all()

    def get_all_helper_observable_ids(self):
        session = self.Session()
        session.close()
        return session.query(HelperTemplateIDs).all()

    def get_helper_for_describe_sensor(self, station_id, sensor_id, observable_id):
        session = self.Session()
        exists = session.query(HelperTemplateIDs).filter(
            and_(HelperTemplateIDs.station_id == station_id,
                 HelperTemplateIDs.sensor_id == sensor_id,
                 HelperTemplateIDs.observable_id == observable_id
                 ))

        if exists.first() is not None:
            print(exists.first().observable_id)
            session.expunge_all()
            session.close()
            return exists.first()
        else:
            return None

    def get_observations_by_helper_id(self, helper_id):
        session = self.Session()
        exists = session.query(Observations).filter(Observations.helper_observable_id == helper_id)

        if exists.first() is not None:
            session.expunge_all()
            session.close()
            return exists.all()
        else:
            return None


if __name__ == "__main__":
    x = DatabaseHandler()
    x.__get_station_id_by_tags_station_id__(210)
