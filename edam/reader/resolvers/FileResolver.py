from edam.reader.input_resources.InputDocumentResource import InputDocumentResource
from edam.reader.models import Template, MetadataFile
from edam.reader.resolvers.Resolver import Resolver


class FileResolver(Resolver):
    def __init__(self, template: Template, metadata: MetadataFile, input_document: InputDocumentResource):
        self.template = template
        self.metadata = metadata
        self.input_document = input_document

    def timeseries(self):
        return self.input_document

    @property
    def preamble(self) -> str:
        return self.template.preamble

    @property
    def header(self) -> str:
        return self.input_document.header

    def complement_stations_from_preamble(self):
        if self.template.preamble and self.input_document.preamble:
            # station = extract_data_from_preamble(self.metadata.station)
            pass

