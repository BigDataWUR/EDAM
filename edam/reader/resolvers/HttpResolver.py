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

    def input_template_match(self) -> bool:
        pass
