import json
import logging

from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy import Column, Integer, String, Boolean, Float

from edam.reader.base import Base
from edam.reader.models.utilities import update_existing

logger = logging.getLogger('edam.reader.models.station')


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
            station is situated. TODO: Obsolete??
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
        return f'<Name {self.name!r}>'
