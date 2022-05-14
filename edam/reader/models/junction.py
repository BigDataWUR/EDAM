from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from edam.reader.base import Base


class Junction(Base):
    """
    """
    __tablename__ = "Junction"
    id = Column(Integer, primary_key=True)
    abstract_observable_id = Column(
        Integer, ForeignKey('AbstractObservable.id'))
    observable = relationship("AbstractObservable", back_populates="junctions")

    unit_id = Column(Integer, ForeignKey('UnitOfMeasurement.id'))
    unit = relationship("UnitOfMeasurement", back_populates="junctions")

    station_id = Column(Integer, ForeignKey('Station.id'))
    station = relationship("Station", back_populates="junctions")

    sensor_id = Column(Integer, ForeignKey('Sensor.id'))
    sensor = relationship("Sensor", back_populates="junctions")

    def __init__(self, abstract_observable_id=None,
                 unit_id=None, station_id=None, sensor_id=None):
        self.abstract_observable_id = abstract_observable_id
        self.unit_id = unit_id
        self.station_id = station_id
        self.sensor_id = sensor_id

    def __repr__(self):
        return f'<{self.__class__.__name__} with id {self.id!r}>'
