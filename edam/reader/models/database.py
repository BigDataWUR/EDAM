from edam.reader.base import Base, engine
from edam.reader.models.junction import Junction
from edam.reader.models.station import Station
from edam.reader.models.observable import AbstractObservable
from edam.reader.models.sensor import Sensor
from edam.reader.models.unit_of_measurement import UnitOfMeasurement
from edam.reader.models.observation import Observation


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)
