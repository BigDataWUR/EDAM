import csv
import fnmatch
import os
import re
from contextlib import contextmanager

import jinja2schema

from edam import get_logger, home_directory
from edam.reader.regular_expressions import template_file_header, \
    for_loop_variables, var_for_line, start_if, end_if, resample_function
from edam.utilities.exceptions import ErrorWithTemplate

logger = get_logger('edam.reader.models.template')


class Template:
    filename: str
    path: str
    variables: str

    def __init__(self, path=None):
        self.path = path

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def header(self) -> str:
        """Gets the header of template based on a regex

        :rtype: str
        :return: Header as string
        """
        regex_header_from_template_file = re.compile(template_file_header)
        with read_template(self) as template_file_object:
            template_contents = template_file_object.read()

        matches = re.findall(regex_header_from_template_file, template_contents)
        if matches:
            header = matches[0][0].strip("\r\n")
            return header
        logger.warning(f"{self.filename} does not have header")

    @property
    def header_line(self):
        with read_template(self) as f:
            for line_number, line in enumerate(f, 0):
                if self.header in line:
                    return line_number

    @property
    def dataframe_header(self):
        return list(filter(lambda x: x != '',
                           self.stripped_contents.split(self.delimiter)))

    @property
    def used_columns(self):
        columns = list(filter(lambda x: x != '',
                              self.stripped_contents.split(self.delimiter)))
        used_columns = list()
        for column in columns:
            variable = jinja2schema.infer(column)
            if len(variable.keys()) > 0:
                for key, value in variable.items():
                    attribute = list(value.keys()).pop()
                    if attribute == "value":
                        used_columns.append(f"{key}")
                    else:
                        used_columns.append(f"{key}.{attribute}")
            else:
                used_columns.append(column)
        return used_columns

    @property
    def variables(self) -> [str]:
        variables = jinja2schema.infer(self.cleaned_contents)
        return list(variables.keys())

    @property
    def observable_ids(self) -> [str]:
        """
           This function parses a template file and returns
           the variables for the template in "for loop" (i.e. observable_id's).
           It returns a list with the variables

           This function is useful for "viewing" purposes.
           A user can submit a query to the web portal and find
           all available templates along with the corresponding observable_id's

           :rtype: [str]
           :return: List of observable IDs
        """
        with read_template(self) as template_file_object:
            template_contents = template_file_object.read()
        matches = re.findall(for_loop_variables, template_contents)
        if matches:
            template_observables = matches[0][0]  # type: str
            self.resampled = matches[0][1]
            template_observables_as_list = list(
                map(lambda observable: observable.rstrip().lstrip(),
                    template_observables.split(',')))

            return template_observables_as_list
        raise ErrorWithTemplate(f"I couldn't extract variables from "
                                f"{self.filename} located at {self.path}")

    @property
    def resampled(self) -> dict:
        """
        """
        return self._resampled

    @resampled.setter
    def resampled(self, value):
        matches = re.findall(resample_function, value)
        dictionary = {}
        if matches:
            try:
                rule = matches[0][0]
            except:
                rule = None
            try:
                how = matches[0][1]
            except:
                rule = None
            dictionary['rule'] = rule
            dictionary['how'] = how
            self._resampled = dictionary
        else:
            self._resampled = None

    @property
    def preamble(self) -> str:
        """
        Gets the template's preamble text (if applicable)
        :return:
        """
        with read_template(self) as template_file_object:
            template_contents = template_file_object.read()

        preamble, _, _ = template_contents.partition(self.header)
        preamble = preamble.rstrip('\n\r')
        if preamble == "":
            return None
        return preamble

    @property
    def stripped_contents(self) -> str:
        with read_template(self) as template_file_object:
            template_contents = template_file_object.read()
        matches = re.findall(var_for_line, template_contents)
        try:
            return matches.pop().lstrip('\n\r').rstrip('\n\r')
        except Exception as exc:
            raise ErrorWithTemplate(exc)

    @property
    def cleaned_contents(self):
        temp = re.sub(start_if, '', self.stripped_contents)
        temp = re.sub(end_if, '', temp).lstrip('\r\n').rstrip('\r\n')
        return temp

    @property
    def delimiter(self) -> str:
        dialect = csv.Sniffer().sniff(self.cleaned_contents)
        return str(dialect.delimiter)

    @property
    def name(self) -> str:
        return self.filename.split('.tmpl')[0]

    def to_dict(self):
        temp = {}
        properties = ['delimiter', 'filename', 'header', 'header_line',
                      'variables']
        for prop in properties:
            try:
                temp[prop] = self.__getattribute__(prop)
            except Exception as e:
                logger.exception("Exception: ")
                temp[prop] = "ERROR"
        return temp

    @property
    def contents(self):
        with read_template(self) as template_file_object:
            return template_file_object.read()

    def __repr__(self):
        return f"{self.filename} located at {self.path}"


@contextmanager
def read_template(template: Template):
    """
    Returns the templates file object
    :rtype: typing.TextIO
    :param template:
    """
    f = open(template.path, 'r')
    yield f
    f.close()


def find_templates_in_directory(directory: str = home_directory) -> [Template]:
    """
        Returns a list of templates located in a given directory.
        Directory defaults to the home_directory(~/.edam)
        :rtype: [Template]
        :param directory: Directory to search for templates
        :return: list of Template objects
    """
    list_of_templates = list()
    for folder, _, files in os.walk(os.path.join(directory, 'templates')):
        for file in files:
            if fnmatch.fnmatch(file, '*.tmpl'):
                path = os.path.join(folder, file)
                filename, _ = os.path.splitext(file)
                templ = Template(path=path)
                list_of_templates.append(templ)
    return list_of_templates
