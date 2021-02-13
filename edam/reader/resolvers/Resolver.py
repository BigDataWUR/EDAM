from abc import ABC, abstractmethod

import pandas as pd


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
    def timeseries(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def template_matches_input(self) -> bool:
        pass
