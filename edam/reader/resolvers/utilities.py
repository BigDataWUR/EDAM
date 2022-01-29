import itertools
import re
from datetime import datetime

from influxdb_client import WritePrecision
import influxdb_client
from influxdb_client.client.write_api import PointSettings, \
    WriteOptions, WriteType
import pandas as pd

from edam.reader.resolvers.Resolver import Resolver

bucket = "edam"
org = "my-org"
token = ""
# Store the URL of your InfluxDB instance
url = "http://127.0.0.1:8086"


def store_data(resolver: Resolver):
    for measurement, dataframe in resolver.timeseries.items():
        dataframe.index = pd.to_datetime(dataframe.index, unit='s')
        try:
            sensor = resolver.metadata.sensors[measurement].name
        except:
            sensor = f"Unknown {measurement} sensor"
        point_settings = PointSettings()
        point_settings.add_default_tag("station", resolver.metadata.station.name)
        point_settings.add_default_tag("sensor", sensor)
        with influxdb_client.InfluxDBClient(url=url,
                                            token=token,
                                            org=org,
                                            enable_gzip=True) as client:
            with client.write_api(
                    write_options=WriteOptions(WriteType.batching,
                                               batch_size=15_000,
                                               flush_interval=10_000),
                    point_settings=point_settings) as write_client:
                write_client.write(bucket=bucket, org=org, record=dataframe.to_frame(),
                                   write_precision=WritePrecision.S,
                                   data_frame_measurement_name=resolver.metadata.station.name)


def retrieve_data(resolver: Resolver):
    with influxdb_client.InfluxDBClient(url=url,
                                        token=token,
                                        org=org, enable_gzip=True) as client:
        query_api = client.query_api()
        buckets = influxdb_client.BucketsApi(client)
        # client.get_list_measurements()
        now = datetime.now()
        query = f'from(bucket:"edam")\
        |> range(start: 1980-01-01T00:00:00Z)\
        |> filter(fn:(r) => r._measurement == "{resolver.metadata.station.name}")\
        |> filter(fn:(r) => r._field == "dewp")\
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
        dataframe = query_api.query_data_frame(query=query, org=org)
        then = datetime.now()
        speed = (then - now).total_seconds()
        print("x")


def extract_station_from_preamble(resolver: Resolver):
    station_dictionary = dict()
    station_dictionary['tags'] = dict()
    station_dictionary['qualifiers'] = dict()
    var_name = r"({{.*?}})"
    for template_line, input_line in itertools.zip_longest(resolver.template.preamble.split('\n'),
                                                           resolver.preamble.split('\n')):
        if template_line:
            matches = re.findall(var_name, template_line)

            if matches:
                for match in matches:

                    # input_line = 'Location: 359800E 223800N, Lat 51.911 Lon -2.584, 67 metres amsl'
                    template_line = template_line.lstrip('')
                    input_line = input_line.lstrip('')
                    # template_line = 'Location: 359800E 223800N, Lat {{station.latitude}} Lon
                    # {{station.longitude}}, {{station.tags.altitude}}'

                    # new_template_line = ' Lon {{station.longitude}}, {{station.tags.altitude}}'

                    # to_be_replaced = 'Location: 359800E 223800N, Lat'
                    to_be_replaced = template_line.partition(match)[
                        0].strip('\n\r')
                    template_line = template_line.partition(
                        match)[-1].strip('\n\r')

                    # value_of_placeholder = input_line.partition(template_line.partition('{')[0])[0]
                    if to_be_replaced.strip(' ') == "":
                        value_of_placeholder = input_line
                    else:
                        value_of_placeholder = input_line.replace(to_be_replaced, '').strip(
                            '\n\r')
                    # print(value_of_placeholder)
                    temp_more_curly = template_line.partition('{')[
                        0].strip('\n\r')

                    if temp_more_curly == '':
                        pass
                    else:
                        input_line = value_of_placeholder
                        value_of_placeholder = value_of_placeholder.partition(temp_more_curly)[
                            0]
                        input_line = input_line.replace(
                            value_of_placeholder, '')

                    # eg ['station', 'latitude'] or ['station', 'tags', 'key']
                    placeholder_var_in_list = match.strip("{}").split('.')
                    # remove 'station', ie first element
                    del placeholder_var_in_list[0]
                    # Now it should be either ['latitude'] or ['tags',
                    # 'key']
                    if placeholder_var_in_list[0] in ['tags', 'qualifiers']:
                        station_dictionary[placeholder_var_in_list[0]][
                            placeholder_var_in_list[-1]] = value_of_placeholder
                    else:
                        station_dictionary[placeholder_var_in_list[0]] = value_of_placeholder

    return station_dictionary
