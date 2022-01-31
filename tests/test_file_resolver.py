import os

import pytest

from edam.reader.models.metadata import Metadata
from edam.reader.models.template import Template
from edam.reader.resolvers.file_resolver import FileResolver
from tests import resources


@pytest.fixture
def input_without_preamble():
    metadata = Metadata(
        path=os.path.join(resources, 'metadata', 'Agmip.yaml'))
    template = Template(
        path=os.path.join(resources, "templates", "Agmip.tmpl"))
    input_uri = os.path.join(resources, "inputs", "Agmip.csv")
    return FileResolver(input_uri=input_uri, template=template,
                        metadata=metadata)


@pytest.fixture
def input_with_preamble():
    metadata = Metadata(
        path=os.path.join(resources, 'metadata', 'uk.yaml'))
    template = Template(
        path=os.path.join(resources, "templates", "uk.tmpl"))
    input_uri = os.path.join(resources, "inputs", "uk.txt")
    return FileResolver(input_uri=input_uri, template=template,
                        metadata=metadata)


def test_timeseries(input_without_preamble):
    timeseries = input_without_preamble.timeseries
    assert len(timeseries) == len(input_without_preamble.template.variables) - 1


def test_non_existing_preamble(input_without_preamble):
    assert input_without_preamble.preamble == ''


def test_header_correct(input_without_preamble):
    real_header = "@DATE    YYYY  MM  DD  SRAD  TMAX  TMIN  RAIN  " \
                  "WIND  DEWP  VPRS  RHUM"

    assert input_without_preamble.header == real_header


def test_complement_stations_from_preamble(input_with_preamble):
    assert input_with_preamble.metadata.station.name == "Armagh"
