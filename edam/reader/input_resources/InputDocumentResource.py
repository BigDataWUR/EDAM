from edam.reader.models import Template
from edam.utilities.exceptions import TemplateInputHeaderMismatch


class InputDocumentResource:
    def __init__(self, file_uri, resource_type, template: Template):
        self.file_contents = file_uri
        self.resource_type = resource_type
        self.associated_template = template
        self.__file_uri = file_uri

    @property
    def file_contents(self):
        return self._file_contents

    @file_contents.setter
    def file_contents(self, file_uri: str):
        with open(file_uri, 'r') as f:
            self._file_contents = f.read()

    @property
    def preamble(self):
        pass

    @property
    def header(self):
        template_header_line = self.associated_template.header_line
        with open(self.__file_uri, 'r') as f:
            for index, line in enumerate(f):
                if index == int(template_header_line):
                    header = line.strip('\r\n')
                    break

        if self.associated_template.header == header:
            return header
        else:
            raise TemplateInputHeaderMismatch("Template/Input header mismatch.\ntemplate: {template_header}")

    @property
    def timeseries(self):
        pass
