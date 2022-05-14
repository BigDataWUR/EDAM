import io
import itertools
import logging
import os
import re
from typing import TYPE_CHECKING, List
from datetime import datetime
import pandas as pd

from edam.reader.database_handler import add_items, add_item
from edam.reader.models.junction import Junction
from edam.reader.models.observation import Observation

logger = logging.getLogger('edam.reader.resolvers.resolver_utilities')

if TYPE_CHECKING:
    from edam.reader.resolvers.resolver import Resolver


def template_matches_file(template_file: str, input_file: str) -> bool:
    return False


def walk_files_in_directory(directory: str) -> List[str]:
    all_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            all_files.append(os.path.join(root, filename))
    return all_files


def store_data_sqlite(resolver: "Resolver"):
    observations = []
    for measurement, dataframe in resolver.timeseries.items():
        abstract_observable_id = \
            resolver.metadata.restructured_metadata[measurement][
                'observable'].id
        sensor_id = resolver.metadata.restructured_metadata[measurement][
            'sensor'].id
        unit_of_measurement_id = \
            resolver.metadata.restructured_metadata[measurement][
                'unit_of_measurement'].id
        station_id = resolver.metadata.station.id
        junction = Junction(abstract_observable_id=abstract_observable_id,
                            unit_id=unit_of_measurement_id,
                            station_id=station_id,
                            sensor_id=sensor_id)
        junction = add_item(junction)  # type: Junction
        for timestamp, value in dataframe.to_dict().items():
            observations.append(Observation(timestamp=timestamp,
                                            value=str(value),
                                            junction_id=junction.id))
    add_items(observations)


def generate_timeseries(resolver: "Resolver") -> [pd.Series]:
    timestamp_columns = list(filter(lambda column: "timestamp." in column,
                                    resolver.template.used_columns))

    contents = resolver.content_as_list[resolver.template.header_line:]
    if contents[0].count(',') == 0:
        contents = '\n'.join(list(
            map(lambda line: re.sub(r'\s+', ',', line.lstrip()).rstrip(
                ',').lstrip(
                ','), contents)))
    else:
        contents = '\n'.join(contents)

    def date_parser(row):
        if "timestamp.dayofyear" in timestamp_columns:
            dt = datetime.strptime(row, "%Y %j")
        else:
            dt = pd.to_datetime(row, errors="coerce")
        return dt

    dataframe_kwargs = {
        'filepath_or_buffer': io.StringIO(contents),
        'names': resolver.template.used_columns,
        'parse_dates': {"timestamp": timestamp_columns},
        'infer_datetime_format': True,
        'na_values': resolver.metadata.station.missing_data,
        'date_parser': date_parser,
        "on_bad_lines": 'warn'
    }
    if resolver.header != '':
        dataframe_kwargs["skiprows"] = [0]

    df = pd.read_csv(**dataframe_kwargs)
    # Drop rows where timestamp was not parsed correctly
    df = df.loc[~df.timestamp.isnull()]
    df.set_index(keys=['timestamp'], inplace=True)
    timeseries = {}
    for variable in resolver.template.variables:
        if variable == "timestamp":
            continue
        timeseries[variable] = df[variable]
        qualifiers = resolver.metadata.station.qualifiers.items()
        for qualifier_name, qualifier in qualifiers:
            if qualifier_name == "missing_data":
                continue

            timeseries[variable] = timeseries[variable].apply(
                lambda x: str(x).rstrip(qualifier))
        if timeseries[variable].dtype is not float:
            timeseries[variable] = timeseries[variable].apply(
                lambda x: float(x))
    return timeseries


def extract_station_from_preamble(resolver: "Resolver"):
    station_dictionary = dict()
    station_dictionary['tags'] = dict()
    station_dictionary['qualifiers'] = dict()
    var_name = r"({{.*?}})"
    for template_line, input_line in itertools.zip_longest(
            resolver.template.preamble.split('\n'),
            resolver.preamble.split('\n')):
        if template_line:
            matches = re.findall(var_name, template_line)

            if matches:
                for match in matches:

                    # input_line = 'Location: 359800E 223800N,
                    # Lat 51.911 Lon -2.584, 67 metres amsl'
                    template_line = template_line.lstrip('')
                    input_line = input_line.lstrip('')
                    # template_line = 'Location: 359800E 223800N,
                    # Lat {{station.latitude}} Lon
                    # {{station.longitude}}, {{station.tags.altitude}}'

                    # new_template_line = ' Lon {{station.longitude}},
                    # {{station.tags.altitude}}'

                    # to_be_replaced = 'Location: 359800E 223800N, Lat'
                    to_be_replaced = template_line.partition(match)[
                        0].strip('\n\r')
                    template_line = template_line.partition(
                        match)[-1].strip('\n\r')

                    # value_of_placeholder =
                    # input_line.partition(template_line.partition('{')[0])[0]
                    if to_be_replaced.strip(' ') == "":
                        value_of_placeholder = input_line
                    else:
                        value_of_placeholder = input_line.replace(
                            to_be_replaced, '').strip(
                            '\n\r')
                    # print(value_of_placeholder)
                    temp_more_curly = template_line.partition('{')[
                        0].strip('\n\r')

                    if temp_more_curly == '':
                        pass
                    else:
                        input_line = value_of_placeholder
                        value_of_placeholder = \
                            value_of_placeholder.partition(temp_more_curly)[
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
                        station_dictionary[
                            placeholder_var_in_list[0]] = value_of_placeholder

    return station_dictionary
