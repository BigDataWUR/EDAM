from edam.reader.models import Template, Metadata
from edam.reader.resolvers.Resolver import Resolver


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
