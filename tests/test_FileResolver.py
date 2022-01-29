import os

import pytest

from edam.reader.models.Metadata import Metadata
from edam.reader.models.Template import Template
from edam.reader.resolvers.FileResolver import FileResolver
from tests import resources_folder


@pytest.fixture
def input_without_preamble():
    metadata = Metadata(path=os.path.join(resources_folder, 'metadata', 'Agmip.yaml'))
    template = Template(path=os.path.join(resources_folder, "templates", "Agmip.tmpl"))
    input_uri = os.path.join(resources_folder, "inputs", "Agmip.csv")
    return FileResolver(input_uri=input_uri, template=template, metadata=metadata)


@pytest.fixture
def input_with_preamble():
    metadata = Metadata(path=os.path.join(resources_folder, 'metadata', 'uk.yaml'))
    template = Template(path=os.path.join(resources_folder, "templates", "uk.tmpl"))
    input_uri = os.path.join(resources_folder, "inputs", "uk1.txt")
    return FileResolver(input_uri=input_uri, template=template, metadata=metadata)


def test_timeseries(input_without_preamble):
    timeseries = input_without_preamble.timeseries
    assert len(timeseries) == len(input_without_preamble.template.variables) - 1


def test_non_existing_preamble(input_without_preamble):
    assert input_without_preamble.preamble is None


def test_header_correct(input_without_preamble):
    real_header = "@DATE    YYYY  MM  DD  SRAD  TMAX  TMIN  RAIN  WIND  DEWP  VPRS  RHUM"

    assert input_without_preamble.header == real_header


def test_complement_stations_from_preamble(input_with_preamble):
    assert input_with_preamble.metadata.station.name == "Armagh"
