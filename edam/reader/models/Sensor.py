import json
import logging

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from edam.reader.base import Base

module_logger = logging.getLogger('edam.reader.models')


class Sensor(Base):
    __tablename__ = "Sensor"
    """
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    manufacturer = Column(String(60))
    tags = Column(String(500))

    abstract_observable_id = Column(
        Integer, ForeignKey('AbstractObservable.id'))
    abstract_observable = relationship("AbstractObservable", back_populates="sensors")

    def update(self, new_data_in_dict):
        for key, value in new_data_in_dict.items():
            try:
                setattr(self, key, value)
            except:
                module_logger.warning("{key} does not exist".format(key=key))
                pass

    def __init__(self,
                 name=None,
                 manufacturer=None,
                 abstract_observable_id=None,
                 tags=json.dumps({})):
        self.name = name
        self.manufacturer = manufacturer
        self.abstract_observable_id = abstract_observable_id
        self.tags = json.dumps(tags)

    def __repr__(self):
        return f'<id {self.id!r}>'
