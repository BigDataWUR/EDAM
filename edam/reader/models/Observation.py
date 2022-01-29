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

    def __init__(self,
                 timestamp=None,
                 value=None,
                 abstract_observable_id=None,
                 unit_id=None,
                 station_id=None,
                 sensor_id=None):
        """
        :param timestamp:
        :param value:
        """
        self.timestamp = timestamp
        self.value = value
        self.abstract_observable_id = abstract_observable_id
        self.unit_id = unit_id
        self.station_id = station_id
        self.sensor_id = sensor_id

    def __repr__(self):
        return f'<id {self.id!r}>'
