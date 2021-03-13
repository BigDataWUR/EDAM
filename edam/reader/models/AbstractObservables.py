import logging

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from edam.reader.database import Base

module_logger = logging.getLogger('edam.reader.models')


class AbstractObservables(Base):
    __tablename__ = "AbstractObservables"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    ontology = Column(String(160))

    obs1 = relationship(
        'HelperTemplateIDs',
        backref='observable',
        lazy='dynamic')

    def __init__(self, name="Temperature", ontology=None, **kwargs):
        self.name = name
        self.ontology = ontology
