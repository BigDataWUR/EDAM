import logging

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from edam.reader.database import Base

module_logger = logging.getLogger('edam.reader.models')


class Observations(Base):
    __tablename__ = "Observations"
    """

    """
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    value = Column(String(60))
    helper_observable_id = Column(Integer, ForeignKey('HelperTemplateIDs.id'))

    def __init__(self, timestamp=None, value=None, helper_observable_id=None):
        """
        :param timestamp:
        :param value:
        :param flag:
        :param tags:
        """
        self.timestamp = timestamp
        self.value = value
        self.helper_observable_id = helper_observable_id

    def __repr__(self):
        return '<id %r>' % self.id
