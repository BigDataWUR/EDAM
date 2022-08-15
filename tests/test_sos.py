import pytest

from edam.services.sos.sos import OgcSos


@pytest.fixture
def sos_object() -> OgcSos:
    pass
    # return OgcSos()


def test_resolve_request_correct():
    assert True


def test_get_capabilities():
    assert True


def test_describe_sensor():
    assert True


def test_get_observation():
    assert True
