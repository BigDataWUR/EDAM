from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from edam.reader.base import Base


class TagJunction(Base):
    __tablename__ = "TagJunction"
    id = Column(Integer, primary_key=True)
    abstract_observable_id = Column(
        Integer, ForeignKey('AbstractObservable.id'))
    unit_id = Column(Integer, ForeignKey('UnitOfMeasurement.id'))
    station_id = Column(Integer, ForeignKey('Station.id'))
    sensor_id = Column(Integer, ForeignKey('Sensor.id'))

    # start_date = Column(DateTime)
    # end_date = Column(DateTime)
    # number_of_observations = Column(Integer)
    # frequency = Column(String(10))
    observable = relationship('AbstractObservable')
    station = relationship('Station',
                           back_populates="helper", cascade="all", single_parent=True)
    # helper_observable_id = relationship(
    #     'Observations', backref='helper', lazy='dynamic')

    def update_metadata(self, metadata_in_dict):
        # TODO: If we append values, we have to change number of observations
        allowed = (
            'start_date',
            'end_date',
            'frequency',
            'number_of_observations')
        start_date_value = getattr(self, 'start_date')
        observations = getattr(self, 'number_of_observations')
        for key, value in metadata_in_dict.items():
            if key in allowed:

                if key == 'start_date' and start_date_value:
                    pass
                elif key == 'number_of_observations' and observations:
                    setattr(self, key, int(value) + observations)
                else:
                    setattr(self, key, value)

    def __init__(self, observable_id=None, sensor_id=None,
                 abstract_observable_id=None, unit_id=None,
                 station_id=None):
        self.observable_id = observable_id
        self.sensor_id = sensor_id
        self.abstract_observable_id = abstract_observable_id
        self.unit_id = unit_id
        self.station_id = station_id

        self.start_date = None
        self.end_date = None
        self.number_of_observations = None
        self.frequency = None

    def __repr__(self):
        return f'<id {self.id!r}>'
