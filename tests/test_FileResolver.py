import os

import pytest

from edam.reader.models import MetadataFile, Template
from edam.reader.resolvers.FileResolver import FileResolver
from tests import resources_folder


@pytest.fixture
def input_document_resource():
    metadata = MetadataFile(path=os.path.join(resources_folder, 'metadata', 'Agmip.yaml'))
    template = Template(path=os.path.join(resources_folder, "templates", "Agmip.tmpl"))
    input_uri = os.path.join(resources_folder, "inputs", "Agmip.csv")
    return FileResolver(input_uri=input_uri, template=template, metadata=metadata)


def test_timeseries():
    assert False


def test_non_existing_preamble(input_document_resource):
    assert input_document_resource.preamble is None


def test_header_correct(input_document_resource):
    real_header = "@DATE    YYYY  MM  DD  SRAD  TMAX  TMIN  RAIN  WIND  DEWP  VPRS  RHUM"

    assert input_document_resource.header == real_header


def test_complement_stations_from_preamble():
    assert False
