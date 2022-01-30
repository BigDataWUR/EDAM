import io
import re

import pandas as pd

from edam.reader.models.metadata import Metadata
from edam.reader.models.template import Template
from edam.reader.resolvers.resolver import Resolver
from edam.reader.resolvers.utilities import extract_station_from_preamble, \
    store_data_sqlite
from edam.utilities.exceptions import TemplateInputHeaderMismatch


class FileResolver(Resolver):
    def __init__(self, input_uri, template: Template, metadata: Metadata):
        self.template = template
        self.metadata = metadata
        self.input_uri = input_uri
        self.content_as_list = input_uri
        self.complement_stations_from_preamble()

    def store_timeseries(self):
        store_data_sqlite(resolver=self)

    def template_matches_input(self) -> bool:
        return True

    @property
    def timeseries(self):
        timestamp_columns = list(filter(lambda column: "timestamp." in column,
                                        self.template.used_columns))

        contents = self.content_as_list[self.template.header_line:]
        if contents[0].count(',') == 0:
            contents = '\n'.join(list(
                map(lambda line: re.sub(r'\s+', ',', line).rstrip(',').lstrip(
                    ','), contents)))
        else:
            contents = '\n'.join(contents)
        if self.header != '':
            df = pd.read_csv(io.StringIO(contents),
                             names=self.template.used_columns, skiprows=[0],
                             parse_dates={"timestamp": timestamp_columns},
                             na_values=self.metadata.station.missing_data)
        else:
            df = pd.read_csv(io.StringIO(contents),
                             names=self.template.used_columns,
                             parse_dates={"timestamp": timestamp_columns},
                             na_values=self.metadata.station.missing_data)
        df.set_index(keys=['timestamp'], inplace=True)
        timeseries = {}
        for variable in self.template.variables:
            if variable == "timestamp":
                continue
            timeseries[variable] = df[variable]
            for qualifier_name, qualifier in self.metadata.station.qualifiers.items():
                if qualifier_name == "missing_data":
                    continue
                if timeseries[variable].dtype is not float:
                    timeseries[variable] = timeseries[variable].apply(
                        lambda x: float(str(x).rstrip(qualifier)))
        return timeseries

    @property
    def preamble(self) -> str:
        preamble = ''.join(self.content_as_list[:self.template.header_line])
        if preamble == '':
            return ''
        return preamble

    def complement_stations_from_preamble(self):
        if self.template.preamble and self.preamble:
            station_dictionary = extract_station_from_preamble(self)
            station = self.metadata.station
            station.update(station_dictionary)
            self.metadata.station = station

    @property
    def content(self):
        return ''.join(self.content_as_list[self.template.header_line:])

    @property
    def content_as_list(self):
        return self._content_as_list

    @content_as_list.setter
    def content_as_list(self, file_uri):
        with open(file_uri, 'r') as file:
            self._content_as_list = file.readlines()

    @property
    def header(self):
        template_header_line = self.template.header_line
        with open(self.input_uri, 'r') as file:
            for index, line in enumerate(file):
                if index == int(template_header_line):
                    header = line.strip('\r\n')
                    break

        if self.template.header == header:
            return header
        else:
            raise TemplateInputHeaderMismatch(
                f"Template/Input header mismatch.\n"
                f"template: {self.template.header}")

    @property
    def template(self) -> Template:
        return self._template

    @template.setter
    def template(self, value):
        self._template = value

    @property
    def metadata(self) -> Metadata:
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        self._metadata = value
