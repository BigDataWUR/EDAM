from abc import ABC, abstractmethod

import pandas as pd

from edam import get_logger
from edam.reader.models.metadata import Metadata
from edam.reader.models.template import Template
from edam.reader.resolvers.resolver_utilities import generate_timeseries, \
    extract_station_from_preamble, store_data_sqlite
from edam.utilities.exceptions import TemplateInputHeaderMismatch

logger = get_logger('edam.reader.resolvers.resolver')


class Resolver(ABC):
    def __init__(self, input_uri, template: Template, metadata: Metadata):
        self.template = template
        self.metadata = metadata
        self.input_uri = input_uri
        self.content_as_list = input_uri
        if self.template_matches_input():
            self.complement_stations_from_preamble()
        # self.store_timeseries()

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

    @property
    def preamble(self) -> str:
        preamble = '\n'.join(self.content_as_list[:self.template.header_line])
        if preamble == '':
            return ''
        return preamble

    @property
    def header(self) -> list:
        template_header_line = self.template.header_line

        header = None
        for index, line in enumerate(self.content_as_list):
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
    def content(self) -> str:
        return '\n'.join(self.content_as_list[self.template.header_line:])

    @property
    def timeseries(self) -> [pd.DataFrame]:
        return generate_timeseries(self)

    def complement_stations_from_preamble(self):
        if self.template.preamble and self.preamble:
            station_dictionary = extract_station_from_preamble(self)
            station = self.metadata.raw_station
            station.update(station_dictionary)
            self.metadata.station = station

    def template_matches_input(self) -> bool:
        if self.template.header == self.header:
            return True
        return False

    def store_timeseries(self):
        logger.debug(f"Storing timeseries for {self.metadata.station.name}")
        store_data_sqlite(resolver=self)

    @property
    @abstractmethod
    def content_as_list(self) -> []:
        pass

    @content_as_list.setter
    @abstractmethod
    def content_as_list(self, value):
        pass
