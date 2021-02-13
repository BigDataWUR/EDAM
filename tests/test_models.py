import os

import pytest

from edam.reader.models import MetadataFile, Station, Sensors, AbstractObservables, Template
from edam.reader.resolvers.ResolverFactory import ResolverFactory
from edam.utilities.exceptions import InputParameterDoesNotExist
from tests import metadata_folder, resources_folder


def test_metadata_file_filename():
    metadata_object = MetadataFile(path=os.path.join(metadata_folder, 'Agmip.yaml'))
    assert metadata_object.filename == "Agmip.yaml"


def test_metadata_file_contents():
    metadata_object = MetadataFile(path=os.path.join(resources_folder, 'metadata', 'Agmip.yaml'))
    contents = metadata_object.contents
    assert type(contents) is dict and 'Station' in contents.keys() \
           and 'Observables' in contents.keys() and 'Sensors' in contents.keys()


def test_metadata_file_get_stations():
    metadata_object = MetadataFile(path=os.path.join(resources_folder, 'metadata', 'Agmip.yaml'))
    station = metadata_object.station
    assert type(station) is Station


def test_metadata_file_get_sensors():
    metadata_object = MetadataFile(path=os.path.join(resources_folder, 'metadata', 'Agmip.yaml'))
    sensors = metadata_object.sensors
    assert type(sensors) is dict and type(sensors["dewp"]) is Sensors


def test_metadata_file_get_observables():
    metadata_object = MetadataFile(path=os.path.join(resources_folder, 'metadata', 'Agmip.yaml'))
    observables = metadata_object.observables
    assert type(observables) is dict and type(observables["dewp"]) is AbstractObservables


def test_input_uri_http_correct():
    input_url = "https://google.gr"
    test_resolver = ResolverFactory(input_url, None, None)
    assert test_resolver.input_uri == input_url


def test_input_uri_file_correct():
    input_url = os.path.join(resources_folder, "inputs/Agmip.csv")
    template_url = os.path.join(resources_folder, "templates", "Agmip.tmpl")
    metadata_url = os.path.join(resources_folder, "metadata", "Agmip.yaml")
    test_resolver = ResolverFactory(input_url, template_url, metadata_url)
    assert test_resolver.input_uri == input_url


def test_input_uri_folder_correct():
    input_url = os.path.join(resources_folder, "inputs")
    template_url = os.path.join(resources_folder, "templates", "Agmip.tmpl")
    metadata_url = os.path.join(resources_folder, "metadata", "Agmip.yaml")
    test_resolver = ResolverFactory(input_url, template_url, metadata_url)
    assert test_resolver.input_uri == input_url


def test_input_uri_file_incorrect():
    input_url = os.path.join(resources_folder, "inputs/doesnt-exist.csv")
    with pytest.raises(InputParameterDoesNotExist):
        ResolverFactory(input_url, None, None)


def test_input_uri_folder_incorrect():
    input_url = os.path.join(resources_folder, "inputsFAKE/")
    with pytest.raises(InputParameterDoesNotExist):
        ResolverFactory(input_url, None, None)


def test_template_header():
    template_url = os.path.join(resources_folder, "templates", "Agmip.tmpl")
    template_object = Template(path=template_url)
    assert template_object.header == "@DATE    YYYY  MM  DD  SRAD  TMAX  TMIN  RAIN  WIND  DEWP  VPRS  RHUM"


def test_template_preamble():
    template_url = os.path.join(resources_folder, "templates", "Agmip.tmpl")
    template_object = Template(path=template_url)
    assert template_object.preamble == ""


def test_template_contents():
    template_url = os.path.join(resources_folder, "templates", "Agmip.tmpl")
    template_object = Template(path=template_url)
    assert template_object.stripped_contents == "1980001  {{timestamp.year}}   {{timestamp.month}}   {{timestamp.day}}  {{srad.value}}  {{tmax.value}}  {{tmin.value}}   {{rain.value}}   {{wind.value}}   {{dewp.value}}   {{vprs.value}}    {{rhum.value}}"

# def test_input_uri_http_incorrect():
#     input_url = "https://i-dont-exist.com"
#     with pytest.raises(UrlInputParameterDoesNotExist):
#         ResolverFactory(input_url, None, None)


# def test_input_uri():
#     assert False
