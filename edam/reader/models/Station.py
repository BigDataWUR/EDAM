import json
import logging

from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship

from edam.reader.base import Base

module_logger = logging.getLogger('edam.reader.models')


class Station(Base):
    __tablename__ = "Station"
    """
    :var id: A unique id among other Stations
    :var name: The name of the Station
    :var mobile: Boolean, i.e. True of False
    :var polygon: :If mobile=True, then a polygon is given
    :var latitude:
    :var longitude:
    """

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

    helper = relationship("TagJunction", back_populates="station")

    def update(self, new_values: dict):
        for key, value in new_values.items():
            try:
                if key in ['tags', 'qualifiers']:
                    temp = getattr(self, key)  # type: dict
                    try:
                        value.update(temp)
                    except ValueError as e:
                        module_logger.warning(f"{e}")
                setattr(self, key, value)
            except AttributeError:
                module_logger.warning(f"{key} does not exist")

    def __init__(self,
                 name=None, mobile=False,
                 location=None, latitude=None,
                 longitude=None, region=None,
                 license=None, url=None,
                 qualifiers=None, tags=None):
        """
        :param name:
        :param mobile:
        :param latitude:
        :param longitude:
        :param tags:
        """
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
