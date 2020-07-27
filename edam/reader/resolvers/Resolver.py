from abc import ABC, abstractmethod


class Resolver(ABC):

    @abstractmethod
    def preamble(self) -> str:
        pass

    @abstractmethod
    def complement_stations_from_preamble(self):
        pass

    @abstractmethod
    def header(self) -> list:
        pass

    @abstractmethod
    def timeseries(self):
        pass

    @abstractmethod
    def input_template_match(self) -> bool:
        pass
