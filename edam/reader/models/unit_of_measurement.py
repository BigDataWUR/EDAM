from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from edam.reader.base import Base


class UnitOfMeasurement(Base):
    """
    Represents a unit of measurement.

    This ORM class represents a unit of measurement.

    Attributes:
        name: The name of the unit (e.g. Celcius)
        ontology: An ontology for this unit
        symbol: The symbol for the unit (e.g. C)
    """
    __tablename__ = "UnitOfMeasurement"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    ontology = Column(String(160))
    symbol = Column(String(15))

    junctions = relationship("Junction", back_populates="unit")

    def __init__(self, name=None, ontology=None, symbol=None):
        self.name = name
        self.ontology = ontology
        self.symbol = symbol

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name!r} with id {self.id!r}>'
