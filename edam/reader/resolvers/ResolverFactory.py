import os
from enum import Enum
from os.path import expanduser

import requests

from edam.reader.models.Template import Template
from edam.reader.models.Metadata import Metadata
from edam.reader.resolvers.FileResolver import FileResolver
from edam.reader.resolvers.HttpResolver import HttpResolver
from edam.reader.resolvers.Resolver import Resolver
from edam.utilities.exceptions import UrlInputParameterDoesNotExist, InputParameterDoesNotExist, TemplateDoesNotExist, \
    MetadataFileDoesNotExist


class InputType(Enum):
    FILE = 1
    FOLDER = 2
    DATABASE = 3
    HTTP = 4


class ResolverFactory:
    __input_type = None

    def __init__(self, input_uri, template, metadata_file, **kwargs):
        self.input_uri = input_uri
        self.template = template
        self.metadata_file = metadata_file

    @property
    def input_uri(self):
        return self._input_uri

    @input_uri.setter
    def input_uri(self, value: str):
        if value.startswith("http://") or value.startswith("https://"):
            self.__input_type = InputType.HTTP
            try:
                requests.get(value).raise_for_status()
                self._input_uri = value
            except requests.HTTPError as e:
                raise UrlInputParameterDoesNotExist(
                    "Can't get {input_uri}: {issue}".format(input_uri=value, issue=str(e.args)))
        elif value.__contains__('db'):
            # TODO: implement this check
            pass
        else:
            if os.path.isfile(value):
                # user gave full path
                self._input_uri = os.path.abspath(value)
                self.__input_type = InputType.FILE
            elif os.path.isfile(os.path.join(expanduser("~"), '.edam', 'inputs', value)):
                # user gave relative path inside the ~/edam/input directory
                self._input_uri = os.path.join(expanduser("~"), '.edam', 'inputs', value)
                self.__input_type = InputType.FILE
            elif os.path.isdir(value):
                self._input_uri = os.path.abspath(value)
                self.__input_type = InputType.FOLDER
            elif os.path.isdir(os.path.join(expanduser("~"), '.edam', 'inputs', value)):
                self._input_uri = os.path.join(expanduser("~"), '.edam', 'inputs', value)
                self.__input_type = InputType.FOLDER
            else:
                raise InputParameterDoesNotExist("{input_uri} does not exist".format(input_uri=value))

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        if value:
            if os.path.isfile(value):
                # user gave full path
                self._template = Template(path=os.path.abspath(value))
            elif os.path.isfile(os.path.join(expanduser("~"), '.edam', 'templates', value)):
                # user gave relative path inside the ~/edam/templates directory
                self._template = Template(
                    path=os.path.abspath(os.path.join(expanduser("~"), '.edam', 'templates', value)))
            else:
                raise TemplateDoesNotExist(f"{value} does not exist")
        else:
            raise TemplateDoesNotExist("No template was given")

    @property
    def metadata_file(self):
        return self._metadata_file

    @metadata_file.setter
    def metadata_file(self, value):
        if os.path.isfile(value):
            # user gave full path
            self._metadata_file = Metadata(path=os.path.abspath(value))
        elif os.path.isfile(os.path.join(expanduser("~"), '.edam', 'metadata', value)):
            # user gave relative path inside the ~/edam/templates directory
            self._metadata_file = Metadata(path=os.path.abspath(os.path.join(expanduser("~"),
                                                                                 '.edam', 'metadata', value)))
        else:
            raise MetadataFileDoesNotExist(f"{value} does not exist")

    @property
    def resolver(self) -> Resolver:
        if self.__input_type is InputType.FILE:
            return FileResolver(template=self.template, metadata=self.metadata_file,
                                input_uri=self.input_uri)
        elif self.__input_type is InputType.HTTP:
            return HttpResolver()
            pass