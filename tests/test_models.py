import os

import pytest

from edam.reader.models import MetadataFile, Station, Sensors, AbstractObservables, Template
from edam.reader.resolvers.ResolverFactory import ResolverFactory
from edam.utilities.exceptions import InputParameterDoesNotExist
from tests import metadata_folder, resources_folder


@pytest.fixture
def metadata_object():
    return MetadataFile(path=os.path.join(metadata_folder, 'Agmip.yaml'))


@pytest.fixture
def test_resolver():
    input_url = os.path.join(resources_folder, "inputs/Agmip.csv")
    template_url = os.path.join(resources_folder, "templates", "Agmip.tmpl")
    metadata_url = os.path.join(resources_folder, "metadata", "Agmip.yaml")
    return ResolverFactory(input_url, template_url, metadata_url)


@pytest.fixture
def template_object():
    template_url = os.path.join(resources_folder, "templates", "Agmip.tmpl")
    return Template(path=template_url)


def test_metadata_file_filename(metadata_object):
    assert metadata_object.filename == "Agmip.yaml"


def test_metadata_file_contents(metadata_object):
    contents = metadata_object.contents
    assert type(contents) is dict and 'Station' in contents.keys() \
           and 'Observables' in contents.keys() and 'Sensors' in contents.keys()


def test_metadata_file_get_stations(metadata_object):
    station = metadata_object.station
    assert type(station) is Station


def test_metadata_file_get_sensors(metadata_object):
    sensors = metadata_object.sensors
    assert type(sensors) is dict and type(sensors["dewp"]) is Sensors


def test_metadata_file_get_observables():
    observables = metadata_object.observables
    assert type(observables) is dict and type(observables["dewp"]) is AbstractObservables


def test_input_uri_http_correct():
    input_url = "https://google.gr"
    test_resolver = ResolverFactory(input_url, None, None)
    assert test_resolver.input_uri == input_url


def test_input_uri_file_correct(test_resolver):
    input_url = os.path.join(resources_folder, "inputs/Agmip.csv")
    assert test_resolver.input_uri == input_url


def test_input_uri_folder_correct(test_resolver):
    input_url = os.path.join(resources_folder, "inputs")
    assert test_resolver.input_uri == input_url


def test_input_uri_file_incorrect():
    input_url = os.path.join(resources_folder, "inputs/doesnt-exist.csv")
    with pytest.raises(InputParameterDoesNotExist):
        ResolverFactory(input_url, None, None)


def test_input_uri_folder_incorrect():
    input_url = os.path.join(resources_folder, "inputsFAKE/")
    with pytest.raises(InputParameterDoesNotExist):
        ResolverFactory(input_url, None, None)


def test_template_header(template_object):
    assert template_object.header == "@DATE    YYYY  MM  DD  SRAD  TMAX  TMIN  RAIN  WIND  DEWP  VPRS  RHUM"


def test_template_preamble(template_object):
    assert template_object.preamble is None


def test_template_contents(template_object):
    assert template_object.stripped_contents == "1980001  {{timestamp.year}}   {{timestamp.month}}   {{timestamp.day}}  {{srad.value}}  {{tmax.value}}  {{tmin.value}}   {{rain.value}}   {{wind.value}}   {{dewp.value}}   {{vprs.value}}    {{rhum.value}}"
