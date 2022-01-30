from edam.reader.models import template, metadata
from edam.reader.models.metadata import Metadata
from edam.reader.models.template import Template
from edam.reader.resolvers.resolver import Resolver


class HttpResolver(Resolver):
    @property
    def metadata(self) -> Metadata:
        pass

    @property
    def template(self) -> Template:
        pass

    def store_timeseries(self):
        pass

    @property
    def preamble(self) -> str:
        pass

    def complement_stations_from_preamble(self):
        pass

    @property
    def header(self) -> list:
        pass

    @property
    def timeseries(self):
        pass

    def template_matches_input(self) -> bool:
        pass
