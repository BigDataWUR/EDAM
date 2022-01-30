from abc import ABC, abstractmethod

import pandas as pd

from edam.reader.models.metadata import Metadata
from edam.reader.models.template import Template


class Resolver(ABC):

    @property
    @abstractmethod
    def template(self) -> Template:
        pass

    @property
    @abstractmethod
    def metadata(self) -> Metadata:
        pass

    @property
    @abstractmethod
    def preamble(self) -> str:
        pass

    @property
    @abstractmethod
    def header(self) -> list:
        pass

    @property
    @abstractmethod
    def content(self) -> str:
        pass

    @property
    @abstractmethod
    def timeseries(self) -> [pd.DataFrame]:
        pass

    @abstractmethod
    def complement_stations_from_preamble(self):
        pass

    @abstractmethod
    def template_matches_input(self) -> bool:
        pass

    @abstractmethod
    def store_timeseries(self):
        pass
