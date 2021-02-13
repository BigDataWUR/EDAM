import pandas as pd

from edam.reader.models import Template, MetadataFile
from edam.reader.resolvers.Resolver import Resolver
from edam.utilities.exceptions import TemplateInputHeaderMismatch


class FileResolver(Resolver):
    def __init__(self, input_uri, template: Template, metadata: MetadataFile):
        self.template = template
        self.metadata = metadata
        self.input_uri = input_uri
        self.file_contents = input_uri

    def template_matches_input(self) -> bool:
        pass

    def timeseries(self):
        pass

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
            raise TemplateInputHeaderMismatch("Template/Input header mismatch.\ntemplate: {template_header}")
