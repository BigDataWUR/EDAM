import csv
import logging
import os
import re
from contextlib import contextmanager
from enum import Enum

from sqlalchemy import Column, Integer, String

from edam.reader.database import Base
from edam.reader.regular_expressions import template_file_header, for_loop_variables, var_for_line
from edam.utilities.exceptions import ErrorWithTemplate

module_logger = logging.getLogger('edam.reader.models')


class Template(Base):
    __tablename__ = "Template"
    id = Column(Integer, primary_key=True)
    filename = Column(String(60))
    path = Column(String(360))
    variables = Column(String(400))

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
            # tokenizer = RegexpTokenizer(r'\w+')

            # return tokenizer.tokenize(header)
        module_logger.warning("{template} does not have header".format(template=self.filename))

    @property
    def header_line(self):
        with read_template(self) as f:
            for line_number, line in enumerate(f, 0):
                if self.header in line:
                    return line_number

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
        raise ErrorWithTemplate(f"I couldn't extract variables from {self.filename} located at {self.path}")

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


class StorageType(Enum):
    FILE = 'file'
    MEMORY = 'memory'


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
