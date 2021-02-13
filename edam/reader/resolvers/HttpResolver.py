from edam.reader.resolvers.Resolver import Resolver


class HttpResolver(Resolver):
    def preamble(self) -> str:
        pass

    def complement_stations_from_preamble(self):
        pass

    def header(self) -> list:
        pass

    def timeseries(self):
        pass

    def template_matches_input(self) -> bool:
        pass
