import json
import logging

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from edam.reader.base import Base
from edam.reader.database_handler import update_object

logger = logging.getLogger('edam.reader.models.sensor')


class Sensor(Base):
    __tablename__ = "Sensor"
    """
    Represents a Sensor.

    This ORM class represents a sensor along with its metadata.

    Attributes:
        name: The name of the sensor
        manufacturer: The name of the sensor's manufacturer
        abstract_observable_id: The Foreign Key which connects a sensor with 
            an (abstract) observable
        tags: dict attribute which represents any other tags which are not
            explicitly defined
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    manufacturer = Column(String(60))
    _tags = Column('tags', String(500))

    abstract_observable_id = Column(
        Integer, ForeignKey('AbstractObservable.id'))
    abstract_observable = relationship("AbstractObservable",
                                       back_populates="sensors")

    def update(self, new_values: dict):
        for key, value in new_values.items():
            try:
                if key in ['tags', 'qualifiers']:
                    temp = getattr(self, key)  # type: dict
                    try:
                        value.update(temp)
                    except ValueError as exception:
                        logger.warning(f"{exception}")
                setattr(self, key, value)
            except AttributeError:
                logger.warning(f"{key} does not exist")
        update_object(self)

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
        return f'<id {self.id!r}>'
