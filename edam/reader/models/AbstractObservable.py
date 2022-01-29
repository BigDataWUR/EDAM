from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from edam.reader.base import Base


class AbstractObservable(Base):
    __tablename__ = "AbstractObservable"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    ontology = Column(String(160))

    sensors = relationship("Sensor", back_populates="abstract_observable")

    def __init__(self, name=None, ontology=None, **kwargs):
        self.name = name
        self.ontology = ontology
