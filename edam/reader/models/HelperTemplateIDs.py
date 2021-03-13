import logging

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from edam.reader.database import Base
from edam.reader.models.AbstractObservables import AbstractObservables
from edam.reader.models.Sensors import Sensors
from edam.reader.models.Station import Station
from edam.reader.models.UnitsOfMeasurement import UnitsOfMeasurement

module_logger = logging.getLogger('edam.reader.models')


class HelperTemplateIDs(Base):
    __tablename__ = "HelperTemplateIDs"
    """

    """
    id = Column(Integer, primary_key=True)
    observable_id = Column(String(30))

    abstract_observable_id = Column(
        Integer, ForeignKey('AbstractObservables.id'))
    unit_id = Column(Integer, ForeignKey('UnitsOfMeasurement.id'))
    station_id = Column(Integer, ForeignKey('Station.id'))
    sensor_id = Column(Integer, ForeignKey('Sensors.id'))

    start_date = Column(DateTime)
    end_date = Column(DateTime)
    number_of_observations = Column(Integer)
    frequency = Column(String(10))

    helper = relationship(
        'Station',
        backref="helper",
        cascade="all",
        single_parent=True)
    helper_observable_id = relationship(
        'Observations', backref='helper', lazy='dynamic')

    def update(self, new_data_in_dict):
        for key, value in new_data_in_dict.items():
            try:
                setattr(self, key, value)
            except KeyError:
                module_logger.warning("{key} does not exist".format(key=key))

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

    @staticmethod
    def add_metadata_file(observable_id: str, station: Station, observables: [AbstractObservables]
                          , sensors: [Sensors], units_of_measurement: [UnitsOfMeasurement]):
        pass

    def __repr__(self):
        return '<id %r>' % (self.id)
