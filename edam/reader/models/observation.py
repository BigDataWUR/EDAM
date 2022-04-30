from sqlalchemy import Column, Integer, DateTime, String, ForeignKey

from edam.reader.base import Base


class Observation(Base):
    """
    Represents an observation.

    This ORM class represents an observation. For the time being,
    apart from `value` (in string format) and `timestamp`, we store Foreign
    Keys pointing to the other dimension of the observations. These include,
    the abstract observable, sensor, unit of measurement and station.

    Attributes:
        value: The measurement as string
        timestamp: When the measurement was taken
        abstract_observable_id: FK to the corresponding abstract observable
        unit_id: FK to the corresponding unit of measurement
        station_id: FK to the corresponding station
        sensor_id: FK to the corresponding sensor
    """
    __tablename__ = "Observation"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    value = Column(String(60))
    junction_id = Column(Integer, ForeignKey('Junction.id'))

    def __init__(self, timestamp=None, value=None, junction_id=None):
        self.timestamp = timestamp
        self.value = value
        self.junction_id = junction_id

    def __repr__(self):
        return f'<id {self.id!r}>'
