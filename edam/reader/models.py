import json
import logging

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

module_logger = logging.getLogger('edam.reader.models')


class Station(Base):
    __tablename__ = "Station"
    """
    :var id: A unique id among other Stations
    :var name: The name of the Station
    :var mobile: Boolean, i.e. True of False
    :var polygon: :If mobile=True, then a polygon is given
    :var latitude:
    :var longitude:
    """
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    mobile = Column(Boolean)
    location = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    region = Column(String(200))
    license = Column(String(100))
    url = Column(String(100))
    
    tags = Column(String(500))
    
    station = relationship('HelperTemplateIDs', backref='station', lazy='dynamic')
    
    @classmethod
    def fromdictionary(cls, d):
        allowed = ('name', 'mobile', 'location', 'latitude', 'longitude', 'region', 'license', 'url', 'tags')
        df = {k: v for k, v in d.items() if k in allowed}
        return cls(**df)
    
    def update(self, newdata_in_dict):
        allowed = ('name', 'mobile', 'location', 'latitude', 'longitude', 'region', 'license', 'url', 'tags')
        for key, value in newdata_in_dict.items():
            if key in allowed:
                setattr(self, key, value)
    
    def __init__(self, name="Test Station", mobile=False, location="", latitude=None, longitude=None, region=None,
                 license=None, url=None, tags=json.dumps({})):
        """
        :param name:
        :param mobile:
        :param latitude:
        :param longitude:
        :param tags:
        """
        self.name = name
        self.mobile = mobile
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.region = region
        self.license = license
        self.url = url
        
        self.tags = json.dumps(tags)
    
    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented
    
    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented
    
    def __repr__(self):
        return '<Name %r>' % (self.name)


class AbstractObservables(Base):
    __tablename__ = "AbstractObservables"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    ontology = Column(String(160))
    
    obs1 = relationship('HelperTemplateIDs', backref='observable', lazy='dynamic')
    
    @classmethod
    def fromdictionary(cls, d):
        allowed = ('name', 'ontology')
        df = {k: v for k, v in d.items() if k in allowed}
        return cls(**df)
    
    def __init__(self, name="Temperature", ontology=None):
        self.name = name
        self.ontology = ontology


class UnitsOfMeasurement(Base):
    __tablename__ = "UnitsOfMeasurement"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    ontology = Column(String(160))
    symbol = Column(String(15))
    
    unit_2 = relationship('Sensors', backref='unit', lazy='dynamic')
    unit1 = relationship('HelperTemplateIDs', backref='uom', lazy='dynamic')
    
    @classmethod
    def fromdictionary(cls, d):
        allowed = ('name', 'ontology', 'symbol')
        df = {k: v for k, v in d.items() if k in allowed}
        return cls(**df)
    
    def __init__(self, name=None, ontology=None, symbol=None):
        self.name = name
        self.ontology = ontology
        self.symbol = symbol


class Sensors(Base):
    __tablename__ = "Sensors"
    """

    """
    id = Column(Integer, primary_key=True)
    generic = Column(Boolean)
    name = Column(String(60))
    manufacturer = Column(String(60))
    tags = Column(String(500))
    
    abstract_observable_id = Column(Integer, ForeignKey('AbstractObservables.id'))
    # We may need to omit the following. It does not make any sense to me.
    unit_id = Column(Integer, ForeignKey('UnitsOfMeasurement.id'))
    
    sens1 = relationship('HelperTemplateIDs', backref='sensor', lazy='dynamic')
    
    @classmethod
    def fromdictionary(cls, d):
        allowed = ('generic', 'name', 'manufacturer', 'tags', 'abstract_observable_id', 'unit_id')
        df = {k: v for k, v in d.items() if k in allowed}
        return cls(**df)
    
    def update(self, new_data_in_dict):
        allowed = ('generic', 'name', 'manufacturer', 'tags', 'abstract_observable_id', 'unit_id')
        for key, value in new_data_in_dict.items():
            if key in allowed:
                setattr(self, key, value)
    
    def __init__(self, generic=False, name="Test sensor", manufacturer="Test manufacturer",
                 abstract_observable_id=None, unit_id=None,
                 tags=json.dumps({})):
        self.generic = generic
        self.name = name
        self.manufacturer = manufacturer
        self.abstract_observable_id = abstract_observable_id
        self.unit_id = unit_id
        self.tags = json.dumps(tags)
    
    def __repr__(self):
        return '<id %r>' % (self.id)


class Observations(Base):
    __tablename__ = "Observations"
    """
    
    """
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    value = Column(String(60))
    helper_observable_id = Column(Integer, ForeignKey('HelperTemplateIDs.id'))
    
    @classmethod
    def fromdictionary(cls, d):
        allowed = ('timestamp', 'value', 'helper_observable_id')
        df = {k: v for k, v in d.items() if k in allowed}
        return cls(**df)
    
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
        return '<id %r>' % (self.id)


class HelperTemplateIDs(Base):
    __tablename__ = "HelperTemplateIDs"
    """

    """
    id = Column(Integer, primary_key=True)
    observable_id = Column(String(30))
    
    abstract_observable_id = Column(Integer, ForeignKey('AbstractObservables.id'))
    unit_id = Column(Integer, ForeignKey('UnitsOfMeasurement.id'))
    station_id = Column(Integer, ForeignKey('Station.id'))
    sensor_id = Column(Integer, ForeignKey('Sensors.id'))
    
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    number_of_observations = Column(Integer)
    frequency = Column(String(10))
    
    helper = relationship('Station', backref="helper", cascade="all", single_parent=True)
    helper_observable_id = relationship('Observations', backref='helper', lazy='dynamic')
    
    @classmethod
    def fromdictionary(cls, d):
        allowed = ('observable_id', 'sensor_id', 'station_id', 'abstract_observable_id', 'unit_id')
        df = {k: v for k, v in d.items() if k in allowed}
        return cls(**df)
    
    def update(self, new_data_in_dict):
        allowed = ('observable_id', 'sensor_id', 'station_id', 'abstract_observable_id', 'unit_id')
        for key, value in new_data_in_dict.items():
            if key in allowed:
                setattr(self, key, value)
    
    def update_meta(self, metadata_in_dict):
        # TODO: If we append values, we have to change number of observations
        allowed = ('start_date', 'end_date', 'frequency', 'number_of_observations')
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


class Templates(Base):
    __tablename__ = "Templates"
    id = Column(Integer, primary_key=True)
    filename = Column(String(60))
    path = Column(String(360))
    template_type = Column(String(20))
    for_loop_vars = Column(String(400))
    
    @classmethod
    def fromdictionary(cls, d):
        allowed = ('path', 'filename', 'template_type', 'for_loop_vars')
        df = {k: v for k, v in d.items() if k in allowed}
        return cls(**df)
    
    def __init__(self, path=None, filename=None, template_type=None, for_loop_vars=None):
        self.path = path
        self.filename = filename
        self.template_type = template_type
        self.for_loop_vars = for_loop_vars
