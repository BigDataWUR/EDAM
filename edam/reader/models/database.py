from edam.reader.base import Base, engine
from edam.reader.models.Station import Station
from edam.reader.models.AbstractObservable import AbstractObservable
from edam.reader.models.Sensor import Sensor
from edam.reader.models.UnitOfMeasurement import UnitOfMeasurement
from edam.reader.models.TagJunction import TagJunction
from edam.reader.models.Observation import Observation


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)
