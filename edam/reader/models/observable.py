from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from edam.reader.base import Base


class AbstractObservable(Base):
    """
    Represents an observable.

    This ORM class represents an observable in its abstract form.
    For example, `temperature` is the abstract observable for `temperature_max`
    or `temp_min`, etc.

    Attributes:
        observable_id:
        name: The name of the observable (e.g. Temperature)
        ontology: An ontology for the observable
    """
    __tablename__ = "AbstractObservable"
    id = Column(Integer, primary_key=True)
    observable_id = Column(String(60))
    name = Column(String(60))
    ontology = Column(String(160))

    sensors = relationship("Sensor", back_populates="abstract_observable")

    junctions = relationship("Junction", back_populates="observable")

    def __init__(self, name=None, ontology=None, observable_id=None,
                 **kwargs):
        self.name = name
        self.ontology = ontology
        self.observable_id = observable_id

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name} with id {self.id!r}>'
