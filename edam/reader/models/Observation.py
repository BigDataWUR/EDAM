from sqlalchemy import Column, Integer, DateTime, String, ForeignKey

from edam.reader.base import Base


class Observation(Base):
    __tablename__ = "Observation"
    """

    """
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    value = Column(String(60))
    abstract_observable_id = Column(
        Integer, ForeignKey('AbstractObservable.id'))
    unit_id = Column(Integer, ForeignKey('UnitOfMeasurement.id'))
    station_id = Column(Integer, ForeignKey('Station.id'))
    sensor_id = Column(Integer, ForeignKey('Sensor.id'))

    def __init__(self, timestamp=None, value=None, helper_observable_id=None):
        """
        :param timestamp:
        :param value:
        """
        self.timestamp = timestamp
        self.value = value
        self.helper_observable_id = helper_observable_id

    def __repr__(self):
        return f'<id {self.id!r}>'
