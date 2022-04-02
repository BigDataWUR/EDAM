from sqlalchemy import Column, Integer, String

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

    def __init__(self, name=None, ontology=None, symbol=None):
        self.name = name
        self.ontology = ontology
        self.symbol = symbol
