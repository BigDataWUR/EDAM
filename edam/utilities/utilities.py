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
from edam.reader.models.Station import Station
from edam.reader.models import Template
from edam.settings import database_type, home_directory

logger = logging.getLogger('edam.reader.utilities')


class DatetimeDirectives(Enum):
    year = '%Y'
    month = '%m'
    day = '%d'
    dayofyear = '%j'
    hour = '%H'
    minutes = '%M'
    seconds = '%S'


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


def combine64(years, months=1, days=1, weeks=None, hours=None, minutes=None,
              seconds=None, milliseconds=None, microseconds=None, nanoseconds=None):
    # Above line was added to fix the drawback when in a year column
    # we had a string (e.g. "Site Closed")
    years = pd.to_numeric(years, errors='coerce').dropna().astype(int)
    years = np.asarray(years) - 1970

    try:
        months = pd.to_numeric(months, errors='coerce').dropna().astype(int)
        months = np.asarray(months) - 1
    except AttributeError:
        # It means user didn't give a month parameter!!
        months = np.asarray(months) - 1

    try:
        days = pd.to_numeric(days, errors='coerce').dropna().astype(int)
        days = np.asarray(days) - 1
    except AttributeError:
        # It means user didn't give a day parameter!!
        days = np.asarray(days) - 1
    types = ('<M8[Y]', '<m8[M]', '<m8[D]', '<m8[W]', '<m8[h]',
             '<m8[m]', '<m8[s]', '<m8[ms]', '<m8[us]', '<m8[ns]')
    vals = (years, months, days, weeks, hours, minutes, seconds,
            milliseconds, microseconds, nanoseconds)
    return sum(np.asarray(v, dtype=t) for t, v in zip(types, vals)
               if v is not None)


def extract_data_from_preamble(station: Station, preamble_template: str,
                               preamble_input: str):
    """
    This function extracts station information from preambles.
    Afterwards, station object is updated and is returned
    :param station: models.Station object
    :param preamble_template:
    :param preamble_input:
    :return:
    """
    # Regex to identify placeholder values (e.g. {{station.name}})
    var_name = r"({{.*?}})"
    # Returns 0 (ie False if empty)
    if preamble_template and preamble_input:
        station_dictionary = dict()
        station_dictionary['tags'] = dict()
        preamble_template_list = preamble_template.split('\n')

        preamble_input_list = preamble_input.split('\n')

        for template_line, input_line in itertools.zip_longest(preamble_template_list, preamble_input_list):
            # Sometimes in input file we have more lines than we thought we would have
            # (when we were drafting the template file). Thus, template_file variable is None
            # and program breaks. This is why we have the following if
            if template_line:
                matches = re.findall(var_name, template_line)

                if matches:
                    for match in matches:

                        # input_line = 'Location: 359800E 223800N, Lat 51.911 Lon -2.584, 67 metres amsl'
                        template_line = template_line.lstrip('')
                        input_line = input_line.lstrip('')
                        # template_line = 'Location: 359800E 223800N, Lat {{station.latitude}} Lon
                        # {{station.longitude}}, {{station.tags.altitude}}'

                        # new_template_line = ' Lon {{station.longitude}}, {{station.tags.altitude}}'

                        # to_be_replaced = 'Location: 359800E 223800N, Lat'
                        to_be_replaced = template_line.partition(match)[
                            0].strip('\n\r')
                        template_line = template_line.partition(
                            match)[-1].strip('\n\r')

                        # value_of_placeholder = input_line.partition(template_line.partition('{')[0])[0]
                        if to_be_replaced.strip(' ') == "":
                            value_of_placeholder = input_line
                        else:
                            value_of_placeholder = input_line.replace(to_be_replaced, '').strip(
                                '\n\r')
                        # print(value_of_placeholder)
                        temp_more_curly = template_line.partition('{')[
                            0].strip('\n\r')

                        if temp_more_curly == '':
                            pass
                        else:
                            input_line = value_of_placeholder
                            value_of_placeholder = value_of_placeholder.partition(temp_more_curly)[
                                0]
                            input_line = input_line.replace(
                                value_of_placeholder, '')

                        # eg ['station', 'latitude'] or ['station', 'tags', 'key']
                        placeholder_var_in_list = match.strip("{}").split('.')
                        # remove 'station', ie first element
                        del placeholder_var_in_list[0]
                        # Now it should be either ['latitude'] or ['tags',
                        # 'key']
                        if placeholder_var_in_list[0] == 'tags':
                            station_dictionary['tags'][
                                placeholder_var_in_list[-1]] = value_of_placeholder
                        else:
                            station_dictionary[placeholder_var_in_list[0]
                            ] = value_of_placeholder

        try:
            station_dictionary['tags'] = json.dumps(station_dictionary['tags'])
        except BaseException:
            pass
        station.update(station_dictionary)
    return station


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
        # returning_value = temp_list[0] + remove_template_placeholders_from_string(temp_list[2], separator)
        returning_value = temp_list[0]

    return returning_value


def template_matches_input_file(template_file: Template, data_input: Template):
    """
    We are going to work with every line (i.e. list element) individually.
    Specifically, we are going to check each of the lines against input files.
    If all lines match to Va given input file, it means that we can parse data out of it.

    :param template_file: The name of the template (e.g. Yucheng.tmpl)
    :param data_input: Either data_input filename (e.g. Yucheng.met) or string with content stored in memory
    :return: True in case match is 100% or False in case match is NOT 100%
    """

    # utilities_logger.debug("Template: %s" % template_file.read())

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
            "Can't convert variables to integers %s, %s" % (starting_number, ending_number))
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
    This function generates a URI derivatives out of a URI which contains a variable part (i.e.
    {number-number}). Variable parts are identified with regex.
    A URI may contain more than one variable parts (e.g. http://example.com/{01-02}-{2010-2011}).
    Function should parse them both and generate variable parts **seperately**.
    For the above example, output is:
    - http://example.com/01-2010
    - http://example.com/02-2010
    - http://example.com/01-2011
    - http://example.com/02-2011

    Attention: There may be cases in which we have the **very same** variable part more than one times.
    All these parts should be generated **all-together** (and not seperately).
    Consider the following example: http://www.example.com/{2016-2017}{01-02}/IDCJDW2006.{2016-2017}{01-02}
    We can identify to "clusters": {2016-2017} and {01-02} occuring twice each.

    For the above example, output is:
    - http://www.example.com/201601/IDCJDW2006.201601
    - http://www.example.com/201701/IDCJDW2006.201701
    - http://www.example.com/201602/IDCJDW2006.201602
    - http://www.example.com/201702/IDCJDW2006.201702

    This version supports only for numerical operations.

    It also exports a list of uris based on a static input.
    A URI contains a placeholder (i.e. http://example.com/{$var}).
    User defines also a set of vars ("one, two, three, four").

    For the above example, output is:
    - http://example.com/one
    - http://example.com/two
    - http://example.com/three
    - http://example.com/four

    :param uri: URI with variable member as indicated by \
    user (e.g. http://example.com/{01-09})
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
                    '--extra parameter was not given (Station variables). generate_uri()')
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
