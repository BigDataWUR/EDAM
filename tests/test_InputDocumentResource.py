import os

from edam.reader.input_resources.InputDocumentResource import InputDocumentResource
from edam.reader.models import Template
from tests import inputs_folder, templates_folder

input_document_resource = InputDocumentResource(file_uri=os.path.join(inputs_folder, "Agmip.csv"), resource_type=None,
                                                template=Template(path=os.path.join(templates_folder, 'Agmip.tmpl')))


def test_preamble():
    assert False


def test_header_correct():
    real_header = "@DATE    YYYY  MM  DD  SRAD  TMAX  TMIN  RAIN  WIND  DEWP  VPRS  RHUM"
    assert input_document_resource.header == real_header


def test_timeseries():
    assert False
