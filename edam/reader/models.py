import json
import logging
import os
import re
from contextlib import contextmanager
from enum import Enum

import yaml
from nltk.tokenize import RegexpTokenizer
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from edam.reader.database import Base
from edam.reader.regular_expressions import template_file_header, for_loop_variables
from edam.utilities.exceptions import ErrorWithTemplate

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

    station = relationship(
        'HelperTemplateIDs',
        backref='station',
        lazy='dynamic')

    def update(self, new_values: dict):
        for key, value in new_values.items():
            try:
                setattr(self, key, value)
            except:
                module_logger.warning("{key} does not exist".format(key=key))
                pass

    def __init__(self, name="Test Station", mobile=False, location="", latitude=None,
                 longitude=None, region=None,
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
        return '<Name %r>' % self.name


class AbstractObservables(Base):
    __tablename__ = "AbstractObservables"
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    ontology = Column(String(160))

    obs1 = relationship(
        'HelperTemplateIDs',
        backref='observable',
        lazy='dynamic')

    def __init__(self, name="Temperature", ontology=None, **kwargs):
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

    abstract_observable_id = Column(
        Integer, ForeignKey('AbstractObservables.id'))
    # We may need to omit the following. It does not make any sense to me.
    unit_id = Column(Integer, ForeignKey('UnitsOfMeasurement.id'))

    sens1 = relationship('HelperTemplateIDs', backref='sensor', lazy='dynamic')

    def update(self, new_data_in_dict):
        for key, value in new_data_in_dict.items():
            try:
                setattr(self, key, value)
            except:
                module_logger.warning("{key} does not exist".format(key=key))
                pass

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
        return '<id %r>' % self.id


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
            except:
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
        return f'<id {self.id!r}>'


class MetadataFile:
    def __init__(self, path=None):
        self.path = path

    @property
    def restructured_metadata(self):
        restructured_metadata = dict()
        sensors = self.sensors
        observables = self.observables
        units_of_measurement = self.units_of_measurement
        for observable_id in self.observable_ids:
            restructured_metadata['station'] = self.station
            restructured_metadata[observable_id] = dict()
            restructured_metadata[observable_id]['sensor'] = sensors[observable_id]
            restructured_metadata[observable_id]['observable'] = observables[observable_id]
            restructured_metadata[observable_id]['unit_of_measurement'] = units_of_measurement[observable_id]

        return restructured_metadata

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def contents(self):
        try:
            with open(self.path, 'r') as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            return exc.args

    @property
    def observable_ids(self):
        return list(self.observables.keys())

    @property
    def station(self) -> Station:
        return Station(**self.contents['Station'])

    @property
    def observables(self) -> [AbstractObservables]:
        return {item.pop('observable_id'): AbstractObservables(**item) for item in self.contents['Observables']}

    @property
    def sensors(self):
        sensors = dict()
        for sensor in self.contents['Sensors']:
            relevant_observables = map(lambda rel_obs: rel_obs.strip().lstrip().rstrip(),
                                       sensor.pop('relevant_observables').split(','))
            for observable_id in relevant_observables:
                sensors[observable_id] = Sensors(**sensor)
        return sensors

    @property
    def units_of_measurement(self):
        units_of_measurement = dict()
        for sensor in self.contents['Units of Measurement']:
            relevant_observables = map(lambda rel_obs: rel_obs.strip().lstrip().rstrip(),
                                       sensor.pop('relevant_observables').split(','))
            for observable_id in relevant_observables:
                units_of_measurement[observable_id] = UnitsOfMeasurement(**sensor)
        return units_of_measurement


class Template(Base):
    __tablename__ = "Template"
    id = Column(Integer, primary_key=True)
    filename = Column(String(60))
    path = Column(String(360))
    variables = Column(String(400))

    def __init__(self, path=None):
        self.path = path

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def header(self) -> str:
        """Gets the header of template based on a regex

        :rtype: str
        :return: Header as string
        """
        regex_header_from_template_file = re.compile(template_file_header)
        with read_template(self) as template_file_object:
            template_contents = template_file_object.read()

        matches = re.findall(regex_header_from_template_file, template_contents)
        if matches:
            header = matches[0][0].strip("\r\n")
            return header
            tokenizer = RegexpTokenizer(r'\w+')

            return tokenizer.tokenize(header)
        module_logger.warning("{template} does not have header".format(template=self.filename))

    @property
    def header_line(self):
        with read_template(self) as f:
            for line_number, line in enumerate(f, 0):
                if self.header in line:
                    return line_number

    @property
    def observable_ids(self) -> [str]:
        """
               This function parses a template file and returns
               the variables for the template in "for loop" (i.e. observable_id's).
               It returns a list with the variables

               This function is useful for "viewing" purposes.
               A user can submit a query to the web portal and find
               all available templates along with the corresponding observable_id's

               :rtype: [str]
               :return: List of observable IDs
               """
        with read_template(self) as template_file_object:
            template_contents = template_file_object.read()
        matches = re.findall(for_loop_variables, template_contents)
        if matches:
            template_observables = matches[0][0]  # type: str
            template_observables_as_list = list(
                map(lambda observable: observable.rstrip().lstrip(),
                    template_observables.split(',')))

            return template_observables_as_list
        raise ErrorWithTemplate("I couldn't extract variables from {filename} located at {path}".
                                format(filename=self.filename, path=self.path))

    @property
    def preamble(self) -> str:
        """
        Gets the template's preamble text (if applicable)
        :return:
        """
        with read_template(self) as template_file_object:
            template_contents = template_file_object.read()

        preamble, _, _ = template_contents.partition(self.header)
        preamble = preamble.rstrip('\n\r')
        return preamble

    def __repr__(self):
        return "{name} located at {path}".format(name=self.filename, path=self.path)


class StorageType(Enum):
    FILE = 'file'
    MEMORY = 'memory'


# class VerifiedResource:
#     """
#     Wraps a resource location given as input by a user. This resource location
#     can be: file, folder (i.e. list of files), database, http (url.
#     """
#
#     def __init__(self, path: str, resource_type: InputType):
#         self.path = path
#         self.resource_type = resource_type
#
#     @property
#     def path(self):
#         return self._path
#
#     @path.setter
#     def path(self):
#
#     """
#     This utility function checks if the given `input_parameter` is either a *file* or *folder*.
#     Firstly, it checks if the input_parameter exists.
#     It checks whether the `input_parameter` contains the full path (e.g. ~/user/this/file.txt, or ~/user/folder).
#     In case it doesn't  it searches in the three folders located in user's home path (e.g. ~/.edam/inputs/, etc.)
#
#     :rtype: VerifiedInputParameter
#     :param input_parameter: The name of the file (e.g. Yucheng.met, or ~/user/this/Yucheng.met)
#     :return: VerifiedInputParameter
#     """
#     if os.path.exists(input_parameter):
#         # It means user gave full path. It may be a file or a folder
#         if os.path.isfile(input_parameter):
#
#             return VerifiedInputParameter(path=input_parameter, parameter_type=InputType.FILE)
#         else:
#             # return True, InputType.FOLDER, input_parameter, None
#             return VerifiedInputParameter(path=input_parameter, parameter_type=InputType.FOLDER)
#     else:
#         # It means we have to find it
#         for folder, included_folder, filenames in os.walk(home_directory):
#             if '.viewer' in included_folder:
#                 included_folder.remove('.viewer')
#             temp_path = os.path.join(folder, input_parameter)
#
#             if os.path.exists(temp_path):
#                 # It means user gave full path. It may be a file or a folder
#
#                 if os.path.isfile(temp_path):
#                     return VerifiedInputParameter(path=temp_path, parameter_type=InputType.FILE)
#                 else:
#                     return VerifiedInputParameter(path=input_parameter, parameter_type=InputType.FOLDER)
#
#     raise InputParameterDoesNotExist("{input_param} does not exist".format(input_param=input_parameter))
#
#     def __eq__(self, other):
#         if isinstance(other, self.__class__):
#             return (self.path == other.path) and (self.resource_type == other.resource_type)


class FolderResolver:
    pass


class UrlResolver:
    pass


class DatabaseResolver:
    pass


@contextmanager
def read_template(template: Template):
    """
    Returns the templates file object
    :rtype: typing.TextIO
    :param template:
    """
    f = open(template.path, 'r')
    yield f
    f.close()
