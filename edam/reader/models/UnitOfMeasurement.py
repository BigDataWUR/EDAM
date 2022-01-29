from sqlalchemy import Column, Integer, String

from edam.reader.base import Base


class UnitOfMeasurement(Base):
    __tablename__ = "UnitOfMeasurement"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    ontology = Column(String(160))
    symbol = Column(String(15))

    def __init__(self, name=None, ontology=None, symbol=None):
        self.name = name
        self.ontology = ontology
        self.symbol = symbol
