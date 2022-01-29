import csv
import logging
import os
import re
from contextlib import contextmanager

import jinja2schema

from edam.reader.regular_expressions import template_file_header, for_loop_variables, var_for_line
from edam.utilities.exceptions import ErrorWithTemplate

module_logger = logging.getLogger('edam.reader.models')


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
        module_logger.warning(f"{self.filename} does not have header")

    @property
    def header_line(self):
        with read_template(self) as f:
            for line_number, line in enumerate(f, 0):
                if self.header in line:
                    return line_number

    @property
    def dataframe_header(self):
        return list(filter(lambda x: x != '', self.stripped_contents.split(self.delimiter)))

    @property
    def used_columns(self):
        columns = list(filter(lambda x: x != '', self.stripped_contents.split(self.delimiter)))
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
    def variables(self):
        variables = jinja2schema.infer(self.stripped_contents)
        return variables.keys()

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
            template_observables_as_list = list(
                map(lambda observable: observable.rstrip().lstrip(),
                    template_observables.split(',')))

            return template_observables_as_list
        raise ErrorWithTemplate(f"I couldn't extract variables from "
                                f"{self.filename} located at {self.path}")

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
            return matches.pop()
        except Exception as exc:
            raise ErrorWithTemplate(exc)

    @property
    def delimiter(self) -> property:
        dialect = csv.Sniffer().sniff(self.stripped_contents)
        return dialect.delimiter

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