import copy

import numpy as np
import pandas as pd
from sqlalchemy.dialects import sqlite
from edam.reader.models.station import Station
from edam.reader.models.observation import Observation
from edam.reader.models.observable import AbstractObservable
from edam.reader.models.sensor import Sensor
from edam.reader.base import db_session as session
from edam.reader.base import engine
from edam.utilities.reader_utilities import find_templates_in_directory


class Measurement(object):
    def __init__(self, value, timestamp=None, observable=None,
                 uom=None, station=None, helper=None):
        table = str.maketrans(dict.fromkeys('#*\"'))
        # if str(value).translate(table) == "None":
        #     self.value = "---"
        # else:
        #     self.value = str(value).translate(table)
        self.value = str(value).translate(table)
        self.timestamp = timestamp
        # TODO: Implement those. Observable and uom should be
        # AbstractObservable and model.Uoms respectively
        self.observable = observable
        self.uom = uom
        self.station = station
        self.helper = helper

    def __repr__(self):
        return self.value


class DatabaseHandler(object):

    def retrieve_stations_data(
            self, station: Station, template_for_lines):
        # print(template_for_lines)

        dict_with_relevant_to_station_help_ids = {
            helper.id: helper.observable_id for helper in station.helper}
        sql = session.query(Observation). \
            filter(Observation.helper_observable_id.in_(
            list(dict_with_relevant_to_station_help_ids)))
        sql_literal = str(
            sql.statement.compile(
                dialect=sqlite.dialect(),
                compile_kwargs={
                    "literal_binds": True}))

        df = pd.read_sql_query(sql_literal, engine)

        df['helper_observable_id'] = df['helper_observable_id']. \
            apply(lambda x: dict_with_relevant_to_station_help_ids[x])
        df.drop('id', axis=1, inplace=True)
        df = df.pivot_table(
            index=df.timestamp,
            columns='helper_observable_id',
            values='value',
            aggfunc='first')
        df.reset_index(inplace=True)
        df["timestamp"] = df["timestamp"].apply(lambda x: pd.to_datetime(x))
        df.set_index(keys=["timestamp"], drop=False, inplace=True)

        station_df = copy.deepcopy(df)

        # Convert values to Measurement objects
        observables_list = list(df)
        observables_list.remove('timestamp')
        table = str.maketrans(dict.fromkeys('#*\"'))
        for observable in observables_list:
            df[observable] = df[observable].apply(lambda x: Measurement(x))
            try:
                station_df[observable] = station_df[observable].apply(
                    lambda x: str(x).translate(table))
            except Exception as e:
                print(observable, e.args)
        # TODO: This is soooooo dangerous. Please re-implement......
        station_df = station_df.replace('None', np.nan)
        # station_df = station_df.fillna('---')
        # print(station_df)

        zip_argument = map(lambda x: "df." + x, template_for_lines)

        zip_argument = ",".join(zip_argument)

        zip_argument = eval("zip(%s)" % zip_argument)
        return Station(station, df=station_df), zip_argument

    @staticmethod
    def retrieve_templates():

        return find_templates_in_directory()


if __name__ == "__main__":
    test = DatabaseHandler()
    results = test.retrieve_templates()
    print(results)
