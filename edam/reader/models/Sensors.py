import json
import logging

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from edam.reader.database import Base

module_logger = logging.getLogger('edam.reader.models')


class Sensors(Base):
    __tablename__ = "Sensors"
    """

    """
    id = Column(Integer, primary_key=True)
    generic = Column(Boolean)
    name = Column(String(60))
    manufacturer = Column(String(60))
    tags = Column(String(500))

    abstract_observable_id = Column(
        Integer, ForeignKey('AbstractObservables.id'))
    # We may need to omit the following. It does not make any sense to me.
    unit_id = Column(Integer, ForeignKey('UnitsOfMeasurement.id'))

    sens1 = relationship('HelperTemplateIDs', backref='sensor', lazy='dynamic')

    def update(self, new_data_in_dict):
        for key, value in new_data_in_dict.items():
            try:
                setattr(self, key, value)
            except:
                module_logger.warning("{key} does not exist".format(key=key))
                pass

    def __init__(self, generic=False, name="Test sensor", manufacturer="Test manufacturer",
                 abstract_observable_id=None, unit_id=None,
                 tags=json.dumps({})):
        self.generic = generic
        self.name = name
        self.manufacturer = manufacturer
        self.abstract_observable_id = abstract_observable_id
        self.unit_id = unit_id
        self.tags = json.dumps(tags)

    def __repr__(self):
        return '<id %r>' % self.id
