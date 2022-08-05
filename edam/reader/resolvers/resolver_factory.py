import fnmatch
import os
from enum import Enum
from os.path import expanduser
from typing import List

import requests

from edam import get_logger
from edam.reader.models.metadata import Metadata
from edam.reader.models.template import Template
from edam.reader.resolvers.file_resolver import FileResolver
from edam.reader.resolvers.http_resolver import HttpResolver
from edam.reader.resolvers.resolver import Resolver
from edam.reader.resolvers.resolver_utilities import walk_files_in_directory
from edam.utilities.exceptions import UrlInputParameterDoesNotExist, \
    InputParameterDoesNotExist, TemplateDoesNotExist, \
    MetadataFileDoesNotExist, TemplateInputHeaderMismatch

logger = get_logger('edam.reader.resolvers.resolver_factory')


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
        self.metadata = self.metadata_file
        try:
            self.var = kwargs['var']
        except KeyError:
            pass

    @property
    def input_uri(self):
        return self._input_uri

    @input_uri.setter
    def input_uri(self, value: str):
        if value.startswith("http://") or value.startswith("https://"):
            self.__input_type = InputType.HTTP
            self._input_uri = value
        elif value.__contains__('db'):
            # TODO: implement this check
            pass
        else:
            if os.path.isfile(value):
                # user gave full path
                self._input_uri = os.path.abspath(value)
                self.__input_type = InputType.FILE
            elif os.path.isfile(
                    os.path.join(expanduser("~"), '.edam', 'inputs', value)):
                # user gave relative path inside the ~/edam/input directory
                self._input_uri = os.path.join(expanduser("~"), '.edam',
                                               'inputs', value)
                self.__input_type = InputType.FILE
            elif os.path.isdir(value):
                self._input_uri = os.path.abspath(value)
                self.__input_type = InputType.FOLDER
            elif os.path.isdir(
                    os.path.join(expanduser("~"), '.edam', 'inputs', value)):
                self._input_uri = os.path.join(expanduser("~"), '.edam',
                                               'inputs', value)
                self.__input_type = InputType.FOLDER
            else:
                raise InputParameterDoesNotExist(
                    "{input_uri} does not exist".format(input_uri=value))

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        if value:
            if os.path.isfile(value):
                # user gave full path
                self._template = Template(path=os.path.abspath(value))
            elif os.path.isfile(
                    os.path.join(expanduser("~"), '.edam', 'templates', value)):
                # user gave relative path inside the ~/edam/templates directory
                self._template = Template(
                    path=os.path.abspath(
                        os.path.join(expanduser("~"), '.edam', 'templates',
                                     value)))
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
            self._metadata_file = os.path.abspath(value)
        elif os.path.isfile(
                os.path.join(expanduser("~"), '.edam', 'metadata', value)):
            # user gave relative path inside the ~/edam/templates directory
            self._metadata_file = os.path.abspath(os.path.join(expanduser("~"),
                                                               '.edam',
                                                               'metadata',
                                                               value))
        else:
            raise MetadataFileDoesNotExist(f"{value} does not exist")

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        self._metadata = Metadata(path=value)

    @property
    def resolver(self) -> List[Resolver]:
        if self.__input_type is InputType.FILE:
            return [FileResolver(template=self.template,
                                 metadata=self.metadata,
                                 input_uri=self.input_uri)]
        elif self.__input_type is InputType.HTTP:
            resolvers = []
            try:
                var = self.__getattribute__('var')
            except AttributeError:
                var = None
            if var is not None:
                variables = list(map(lambda item: item.lstrip().rstrip(),
                                     var.split(",")))
                for variable in variables:
                    uri = self.input_uri.replace("{_var_}", variable)
                    try:
                        requests.get(uri).raise_for_status()
                        meta = Metadata(path=self.metadata_file)
                        resolvers.append(HttpResolver(template=self.template,
                                                      metadata=meta,
                                                      input_uri=uri))
                    except requests.HTTPError:
                        logger.exception(f"{variable} station does not exist")
                return resolvers
            else:
                return [HttpResolver(template=self.template,
                                     metadata=self.metadata,
                                     input_uri=self.input_uri)]

        elif self.__input_type is InputType.FOLDER:
            resolvers = []
            for file in walk_files_in_directory(self.input_uri):
                if fnmatch.fnmatch(file, '*.tmpl'):
                    logger.debug(f"Ignore .tmpl file: {file}")
                    continue
                try:
                    meta = Metadata(path=self.metadata_file)
                    temp_resolver = FileResolver(template=self.template,
                                                 metadata=meta,
                                                 input_uri=file)
                    if temp_resolver.template_matches_input():
                        resolvers.append(temp_resolver)
                except TemplateInputHeaderMismatch:
                    logger.warning(
                        f"{self.template.filename} can't parse {file}")
                except UnicodeDecodeError:
                    logger.exception(
                        f"Exception while trying to parse {file} with "
                        f"{self.template.filename}")

            return resolvers
