import os

import pytest

from edam.reader.resolvers.file_resolver import FileResolver
from edam.reader.resolvers.http_resolver import HttpResolver
from edam.reader.resolvers.resolver_factory import ResolverFactory
from tests import inputs_folder, templates_folder, metadata_folder


def test_main_resolver_type_file():
    resolver = ResolverFactory(
        input_uri=os.path.join(inputs_folder, 'Agmip.csv'),
        template=os.path.join(templates_folder, "Agmip.tmpl"),
        metadata_file=os.path.join(metadata_folder, "Agmip.yaml"))
    assert len(resolver.resolver) == 1
    assert type(resolver.resolver.pop()) is FileResolver


@pytest.mark.vcr
def test_main_resolver_type_http():
    resolver = ResolverFactory(
        input_uri="https://www.metoffice.gov.uk/"
                  "pub/data/weather/uk/climate/stationdata/"
                  "aberporthdata.txt",
        template=os.path.join(templates_folder,
                              "uk.tmpl"),
        metadata_file=os.path.join(metadata_folder,
                                   "uk.yaml"))
    assert len(resolver.resolver) == 1
    assert type(resolver.resolver.pop()) is HttpResolver


def test_folder_resolver():
    resolver = ResolverFactory(
        input_uri=os.path.join(inputs_folder),
        template=os.path.join(templates_folder, "uk.tmpl"),
        metadata_file=os.path.join(metadata_folder, "uk.yaml"))
    assert len(resolver.resolver) == 3
