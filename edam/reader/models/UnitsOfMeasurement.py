import logging

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from edam.reader.database import Base

module_logger = logging.getLogger('edam.reader.models')


class UnitsOfMeasurement(Base):
    __tablename__ = "UnitsOfMeasurement"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    ontology = Column(String(160))
    symbol = Column(String(15))

    unit_2 = relationship('Sensors', backref='unit', lazy='dynamic')
    unit1 = relationship('HelperTemplateIDs', backref='uom', lazy='dynamic')

    def __init__(self, name=None, ontology=None, symbol=None):
        self.name = name
        self.ontology = ontology
        self.symbol = symbol
