import json
import logging

from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship

from edam.reader.database import Base

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

    tags = Column(String(500))

    station = relationship(
        'HelperTemplateIDs',
        backref='station',
        lazy='dynamic')

    def update(self, new_values: dict):
        for key, value in new_values.items():
            try:
                setattr(self, key, value)
            except:
                module_logger.warning(f"{key} does not exist")
                pass

    def __init__(self, name="Test Station", mobile=False, location="", latitude=None,
                 longitude=None, region=None,
                 license=None, url=None, tags=json.dumps({})):
        """
        :param name:
        :param mobile:
        :param latitude:
        :param longitude:
        :param tags:
        """
        self.name = name
        self.mobile = mobile
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.region = region
        self.license = license
        self.url = url

        self.tags = json.dumps(tags)

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
