import json
from datetime import datetime

import pandas as pd
from sqlalchemy.dialects import sqlite
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship

from edam import get_logger
from edam.reader.base import Base, session, engine
from edam.reader.models.measurement import Measurement
from edam.reader.models.observation import Observation
from edam.reader.models.utilities import update_existing, as_dict, resample
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from edam.reader.models.template import Template

logger = get_logger('edam.reader.models.station')


class Station(Base):
    """
    Represents a Station.

    This ORM class represents a station along with its metadata.
    According to the EDAM conceptual model, a station can be stationary or
    moving.

    Attributes:
        name: The name of the station
        mobile: Boolean value to define whether it's a stationary or moving
            station
        location: string attribute which describes the location where the
            station is situated
        latitude: float attribute which represent the station's latitude
        longitude: float attribute which represent the station's longitude
        region: string attribute which describes the region where the
            station is situated.
        license: string attribute which represents the license of the data
            that the station holds
        url: string attribute of the station's url (if applicable)
        tags: dict attribute which represents any other tags which are not
            explicitly defined
        qualifiers: dict attribute which represents any qualifiers for the
            station's data. A standard qualifier is `missing_data`. For the
            rest, the `key` of this attribute is the qualifier (e.g. `*`) and
            the `value` the qualifier (e.g. `estimated`)
    """
    __tablename__ = "Station"
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    mobile = Column(Boolean)
    location = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    region = Column(String(200))
    license = Column(String(100))
    url = Column(String(100))
    _tags = Column('tags', String(500))
    _qualifiers = Column('qualifiers', String(500))

    junctions = relationship("Junction", back_populates="station")

    def update(self, new_values: dict):
        update_existing(self, new_values, logger)

    def __init__(self,
                 name: str = None, mobile: bool = False,
                 location: str = None, latitude: float = None,
                 longitude: float = None, region: str = None,
                 license: str = None, url: str = None,
                 qualifiers: dict = None, tags: dict = None):
        if tags is None:
            tags = dict()
        self.name = name
        self.mobile = mobile
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.region = region
        self.license = license
        self.url = url

        self.qualifiers = qualifiers
        self.tags = tags

    @hybrid_property
    def tags(self):
        return json.loads(self._tags)

    @tags.setter
    def tags(self, value):
        self._tags = json.dumps(value)

    @hybrid_property
    def qualifiers(self):
        return json.loads(self._qualifiers)

    @qualifiers.setter
    def qualifiers(self, value):
        if value is None:
            self._qualifiers = json.dumps({})
        else:
            self._qualifiers = json.dumps(value)

    @property
    def missing_data(self):
        try:
            return self.qualifiers['missing_data']
        except KeyError:
            return ''
        except TypeError:
            return ''

    @property
    def observable_ids(self) -> [str]:
        return [junction.observable.observable_id for junction in
                self.junctions]

    @property
    def junctions_mapping(self) -> dict:
        return {junction.id: junction.observable.observable_id for junction in
                self.junctions}

    @property
    def data(self) -> pd.DataFrame:
        dataframes = []
        for junction in self.junctions_mapping.keys():
            sql = session.query(Observation).filter(
                Observation.junction_id == junction)
            sql_literal = str(sql.statement.compile(dialect=sqlite.dialect(),
                                                    compile_kwargs={
                                                        "literal_binds": True}))

            df = pd.read_sql_query(sql_literal, engine)

            df.rename(columns={"value": self.junctions_mapping[junction]},
                      inplace=True)
            if dataframes:
                df.drop(['id', 'junction_id', 'timestamp'], axis=1,
                        inplace=True)
            else:
                df.drop(['id', 'junction_id'], axis=1, inplace=True)
            dataframes.append(df)
        if dataframes:
            dataframe = pd.concat(dataframes, join='inner', axis=1).fillna(
                "empty")  # type: pd.DataFrame
            dataframe.set_index(keys=["timestamp"], drop=False, inplace=True)
            return dataframe
        logger.warning(f"{self.name} does not have any data associated")
        return None

    def data_iter(self, template: "Template"):
        data = self.data
        variables = template.observable_ids
        if template.resampled:
            data = resample(self, template.resampled['rule'],
                            template.resampled['how'])
        for row in data.itertuples():
            if variables is not None:
                yield self._prepare_dataframe_generator(row, variables)
            else:
                yield self._prepare_dataframe_generator(row, list(data))

    def resampled(self, rule=None, how=None):
        return self._res

    @property
    def res(self):
        return self._res

    @res.setter
    def res(self, value):
        self._res = value

    def _prepare_dataframe_generator(self, row: tuple, variables) -> []:
        gen = []
        for variable in variables:
            value = row.__getattribute__(variable)
            if variable == "timestamp":
                gen.append(datetime.strptime(value.split('.')[0],
                                             "%Y-%m-%d %H:%M:%S"))
            else:
                if value == "nan":
                    try:
                        gen.append(Measurement(self.qualifiers['missing_data']))
                    except Exception:
                        gen.append(Measurement(value))
                else:
                    gen.append(Measurement(value))
        return gen

    def as_dict(self):
        return as_dict(self)

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name!r} with id {self.id!r}>'
