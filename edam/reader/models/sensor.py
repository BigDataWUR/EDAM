import json

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from edam import get_logger
from edam.reader.base import Base
from edam.reader.models.utilities import update_existing

logger = get_logger('edam.reader.models.sensor')


class Sensor(Base):
    """
    Represents a Sensor.

    This ORM class represents a sensor along with its metadata.

    Attributes:
        name: The name of the sensor
        manufacturer: The name of the sensor's manufacturer
        tags: dict attribute which represents any other tags which are not
            explicitly defined
    """
    __tablename__ = "Sensor"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    manufacturer = Column(String(60))
    _tags = Column('tags', String(500))

    abstract_observable_id = Column(
        Integer, ForeignKey('AbstractObservable.id'))
    abstract_observable = relationship("AbstractObservable",
                                       back_populates="sensors")

    junctions = relationship("Junction", back_populates="sensor")

    def update(self, new_values: dict):
        update_existing(self, new_values, logger)

    def __init__(self, name: str = None, manufacturer: str = None,
                 abstract_observable_id: int = None,
                 tags: dict = None):
        self.name = name
        self.manufacturer = manufacturer
        self.abstract_observable_id = abstract_observable_id
        self.tags = tags

    @hybrid_property
    def tags(self):
        return json.loads(self._tags)

    @tags.setter
    def tags(self, value):
        self._tags = json.dumps(value)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name} with id {self.id!r}>'
