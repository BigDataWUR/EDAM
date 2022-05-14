import copy
import errno
import fnmatch
import io
import itertools
import json
import logging
import os
import re
from datetime import datetime
from enum import Enum

import numpy as np
import pandas as pd
import records
import requests

# from edam.reader.manage import DatabaseHandler
from edam.reader.models.station import Station
from edam.reader.models import template
from edam.reader.models.template import Template
from edam import database_type, home_directory

logger = logging.getLogger('edam.reader.utilities')


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
                template = Template(path=path)
                list_of_templates.append(template)
    return list_of_templates


def remove_template_placeholders_from_string(string, separator="({.*?}+)"):
    """
    This function cleans a **string** according to a given **separator**.

    :param string: The string which will be cleaned
    :param separator: Regex pattern. $param1 will be cleaned according to this param.
    :return: string: Cleaned string
    """

    temp_list = re.split(separator, string, 1)
    # string does not contain separator. Return as is
    if len(temp_list) == 1:
        returning_value = temp_list[0]
    else:
        # It means it has 3 elements.
        # returning_value = temp_list[0] +
        # remove_template_placeholders_from_string(temp_list[2], separator)
        returning_value = temp_list[0]

    return returning_value


def template_matches_input_file(template_file: Template, data_input: Template):
    """
    We are going to work with every line (i.e. list element) individually.
    Specifically, we are going to check each of the lines against input_file files.
    If all lines match to Va given input_file file, it means that we can parse data
    out of it.

    :param template_file: The name of the template (e.g. Yucheng.tmpl)
    :param data_input: Either data_input filename (e.g. Yucheng.met) or string
    with content stored in memory
    :return: True in case match is 100% or False in case match is NOT 100%
    """

    header = template_file.header
    logger.debug("Check lines: %s")
    matching_percentage = int()

    logger.debug("Input file: %s" % data_input)

    for header_item in header:
        if header_item in ":":
            matching_percentage += 1

    # percentage = float(100 * matching_percentage / len(check_lines))
    percentage = 10
    if percentage > 20:
        return True
    else:
        return False


def evaluate_variable_part(variable):
    """
    This function evaluates a variable (check parameter).
    :param variable:{0-n}
    :return: ['{0-n}': [0, 1, 2, ..., n]]
    """
    initial_var = copy.deepcopy(variable)
    variable = variable.strip('{}').split('-')
    if len(variable) > 2 or len(variable) < 2:
        logger.error('Range %s is not correct in the correct format '
                     '{starting_int - ending_int}' % initial_var)
        raise Exception('Range %s is not correct in the correct format '
                        '{starting_int - ending_int}' % initial_var)

    starting_number = variable[0]
    ending_number = variable[1]

    # We need this one to set the argument of "format" function
    # If we are given 01-03, we should return 01, 02, 03
    # and NOT 1, 2, 3

    length = len(starting_number)
    try:
        starting_number = int(starting_number)
        # range() is not inclusive!
        ending_number = int(ending_number) + 1
    except BaseException:
        logger.error(
            "Can't convert variables to integers %s, %s" % (
                starting_number, ending_number))
        raise Exception("Can't convert variables to integers")

    the_range = range(starting_number, ending_number)
    # e.g. format(x,'02d')
    format_argument = '0' + str(length) + 'd'
    temp_list = [format(x, format_argument) for x in the_range]
    temp_as_a_dict = dict()
    temp_as_a_dict[initial_var] = temp_list

    return temp_as_a_dict


def generate_uri(uri: str, static_variables=None):
    """
    This function generates a URI derivatives out of a URI which contains a
    variable part (i.e. {number-number}). Variable parts are identified
    with regex. A URI may contain more than one variable parts
    (e.g. https://example.com/{01-02}-{2010-2011}).
    Function should parse them both and generate variable parts **seperately**.
    For the above example, output is:
    - https://example.com/01-2010
    - https://example.com/02-2010
    - https://example.com/01-2011
    - https://example.com/02-2011

    Attention: There may be cases in which we have the **very same**
    variable part more than one times. All these parts should be generated
    **all-together** (and not seperately). Consider the following example:
    https://www.example.com/{2016-2017}{01-02}/IDCJDW2006.{2016-2017}{01-02}
    We can identify to "clusters": {2016-2017} and {01-02} occuring twice each.

    For the above example, output is:
    - https://www.example.com/201601/IDCJDW2006.201601
    - https://www.example.com/201701/IDCJDW2006.201701
    - https://www.example.com/201602/IDCJDW2006.201602
    - https://www.example.com/201702/IDCJDW2006.201702

    This version supports only for numerical operations.

    It also exports a list of uris based on a static input_file.
    A URI contains a placeholder (i.e. https://example.com/{$var}).
    User defines also a set of vars ("one, two, three, four").

    For the above example, output is:
    - https://example.com/one
    - https://example.com/two
    - https://example.com/three
    - https://example.com/four

    :param uri: URI with variable member as indicated by \
    user (e.g. https://example.com/{01-09})
    :param static_variables:
    :return: A list with all resulting URIs. In case URI does \
    not contain variable part (i.e. {01-09}), it returns one uri in a list
    """
    # variable_regex is more generic. It matches both {01-09} AND {$var}
    # (i.e. static_variable_regex)
    variable_regex = r"({.*?})"
    static_variable_regex = r"({\$var})"
    match = re.search(variable_regex, uri)
    uris_in_a_list = list()
    if match:
        if re.search(static_variable_regex, uri):
            try:
                # We are in the case we have static variables
                static_variables_in_a_list = static_variables.split(',')
                for static_var in static_variables_in_a_list:
                    iteration_uri = copy.deepcopy(uri)
                    iteration_uri = iteration_uri.replace(
                        "{$var}", static_var.strip())
                    uris_in_a_list.append(iteration_uri)
            except AttributeError:
                logger.error(
                    '--extra parameter was not given (Station variables). '
                    'generate_uri()')
                raise AttributeError(
                    '--extra parameter (static vars) was empty')
        else:
            # We want all unique variable parts. See documentation about
            # clusters!
            variable_parts_in_a_list = list(
                set(re.findall(variable_regex, uri)))
            evaluated_variable_parts = list(
                map(evaluate_variable_part, variable_parts_in_a_list))

            to_be_replaced = list()
            to_replace_with = list()
            for dict_pair in evaluated_variable_parts:
                key, value = dict_pair.popitem()
                to_be_replaced.append(key)
                to_replace_with.append(value)

            to_replace_with = list(itertools.product(*to_replace_with))

            for item in to_replace_with:
                iteration_uri = copy.deepcopy(uri)
                for count, value in enumerate(item):
                    iteration_uri = iteration_uri.replace(
                        to_be_replaced[count], value)
                uris_in_a_list.append(iteration_uri)
    else:
        uris_in_a_list.append(uri)

    return uris_in_a_list


if __name__ == "__main__":
    pass
