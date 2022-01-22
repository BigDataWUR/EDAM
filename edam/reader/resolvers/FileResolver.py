import pandas as pd

from edam.reader.database_handler import add_item, add_items
from edam.reader.models import Template, Metadata
from edam.reader.resolvers.Resolver import Resolver
from edam.utilities.exceptions import TemplateInputHeaderMismatch


class FileResolver(Resolver):
    def __init__(self, input_uri, template: Template, metadata: Metadata):
        self.template = template
        self.metadata = metadata
        self.input_uri = input_uri
        self.file_contents = input_uri
        add_items(self.metadata.sensors.values())
        add_items(self.metadata.observables.values())
        add_items(self.metadata.units_of_measurement.values())
        add_item(self.metadata.station)

    def template_matches_input(self) -> bool:
        pass

    @property
    def timeseries(self):
        timestamp_columns = list(filter(lambda column: "timestamp." in column, self.template.used_columns))
        if self.header != '':
            df = pd.read_fwf(self.input_uri, names=self.template.used_columns, skiprows=[0],
                             parse_dates={"timestamp": timestamp_columns})
        else:
            df = pd.read_fwf(self.input_uri, names=self.template.used_columns,
                             parse_dates={"timestamp": timestamp_columns})
        df.set_index(keys=['timestamp'], inplace=True)
        timeseries = dict()
        for variable in self.template.variables:
            if variable == "timestamp":
                continue
            timeseries[variable] = df[variable]
        return timeseries

    @property
    def preamble(self) -> str:
        return self.template.preamble

    def complement_stations_from_preamble(self):
        if self.template.preamble and self.preamble:
            # station = extract_data_from_preamble(self.metadata.station)
            pass

    @property
    def file_contents(self):
        return self._file_contents

    @file_contents.setter
    def file_contents(self, file_uri: str):
        with open(file_uri, 'r') as f:
            self._file_contents = f.read()

    @property
    def header(self):
        template_header_line = self.template.header_line
        with open(self.input_uri, 'r') as f:
            for index, line in enumerate(f):
                if index == int(template_header_line):
                    header = line.strip('\r\n')
                    break

        if self.template.header == header:
            return header
        else:
            raise TemplateInputHeaderMismatch(f"Template/Input header mismatch.\n"
                                              f"template: {self.template.template_header}")
