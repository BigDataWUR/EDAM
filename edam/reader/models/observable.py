from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from edam.reader.base import Base


class AbstractObservable(Base):
    """
    Represents an observable.

    This is an ORM class which represents an observable in its abstract form.
    For example, `temperature` is the abstract observable for `temperature_max`
    or `temp_min`, etc.

    Attributes:
        name: The name of the observable (e.g. Temperature)
        ontology: An ontology for the observable
    """
    __tablename__ = "AbstractObservable"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    ontology = Column(String(160))

    sensors = relationship("Sensor", back_populates="abstract_observable")

    def __init__(self, name=None, ontology=None):
        self.name = name
        self.ontology = ontology
