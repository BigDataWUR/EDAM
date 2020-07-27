import os

from edam.reader.resolvers.FileResolver import FileResolver
from edam.reader.resolvers.HttpResolver import HttpResolver
from edam.reader.resolvers.ResolverFactory import ResolverFactory
from tests import inputs_folder, templates_folder, metadata_folder


def test_main_resolver_type_file():
    resolver = ResolverFactory(input_uri=os.path.join(inputs_folder, 'Agmip.csv'),
                               template=os.path.join(templates_folder, "Agmip.tmpl"),
                               metadata_file=os.path.join(metadata_folder, "Agmip.yaml"))
    assert type(resolver.resolver) is FileResolver


def test_main_resolver_type_http():
    resolver = ResolverFactory(input_uri="https://google.gr",
                               template=os.path.join(templates_folder, "Agmip.tmpl"),
                               metadata_file=os.path.join(metadata_folder, "Agmip.yaml"))
    assert type(resolver.resolver) is HttpResolver


def test_input_uri():
    assert False


def test_input_uri():
    assert False


def test_template():
    assert False


def test_template():
    assert False


def test_metadata_file():
    assert False


def test_metadata_file():
    assert False


def test_resolver():
    assert False
