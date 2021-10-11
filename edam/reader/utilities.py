import copy
import csv
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
import yaml

from edam.reader.manage import DatabaseHandler
from edam.reader.models import Station
from edam.settings import database_type, home_directory

utilities_logger = logging.getLogger('edam.reader.utilities')


class InputType(Enum):
    FILE = 1
    FOLDER = 2
    DATABASE = 3
    HTTP = 4
    

class StorageType(Enum):
    FILE = 'file'
    MEMORY = 'memory'


def find_and_describe_templates(directory=home_directory):
    temp_dict = dict()
    for fold, _, files in os.walk(os.path.join(directory, 'templates')):
        for file in files:
            filename = os.path.join(fold, file)
            if fnmatch.fnmatch(filename, '*.tmpl'):
                name, ext = os.path.splitext(file)
                temp_dict[name] = dict()
                temp_dict[name]['path'] = filename
                temp_dict[name]['variables'] = get_template_for_vars(open(filename, 'r'))
    
    return temp_dict


def find_and_describe_template(template):
    temp_dict = dict()
    
    exists, file_type, file_path, file_object = check_if_path_exists(template + ".tmpl")
    if exists and file_type is InputType.FILE:
        temp_dict['path'] = file_path
        temp_dict['variables'] = get_template_for_vars(file_object)
        
        return temp_dict
    return None


def combine64(years, months=1, days=1, weeks=None, hours=None, minutes=None,
              seconds=None, milliseconds=None, microseconds=None, nanoseconds=None):
    # Above line was added to fix the drawback when in a year column we had a string (e.g. "Site Closed")
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


def space_delimited_to_csv(input_file: io.StringIO):
    """
    I copied that from:
    http://stackoverflow.com/questions/19759423/convert-a-space-delimited-file-to-comma-separated-values-file-in-python
    
    :param input_file:
    :return:
    """
    input_file.seek(0)
    input_text = input_file
    output_text = io.StringIO()
    o = csv.writer(output_text)
    for line in input_text:
        stripped_line = line.strip('\n')
        # Don't put commas in for loops
        if ("{%for" or "{%endfor}") in stripped_line:
            output_text.write(line)
        else:
            o.writerow(stripped_line.split())
    return output_text


def extract_data_from_preamble(station: Station, preamble_template, preamble_input):
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
    if preamble_template.seek(0, os.SEEK_END) > 0 and preamble_input.seek(0, os.SEEK_END) > 0:
        station_dictionary = dict()
        station_dictionary['tags'] = dict()
        preamble_template.seek(0)
        preamble_input.seek(0)
        ptemp = preamble_template
        
        pinp = preamble_input
        
        for template_line, input_line in itertools.zip_longest(ptemp, pinp):
            # Sometimes in input file we have more lines than we thought we would have
            # (when we were drafting the template file). Thus, template_file variable is None
            # and program breaks. This is why we havethe following if
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
                        to_be_replaced = template_line.partition(match)[0].strip('\n\r')
                        template_line = template_line.partition(match)[-1].strip('\n\r')
                        
                        # value_of_placeholder = input_line.partition(template_line.partition('{')[0])[0]
                        if to_be_replaced.strip(' ') == "":
                            value_of_placeholder = input_line
                        else:
                            value_of_placeholder = input_line.replace(to_be_replaced, '').strip('\n\r')
                        # print(value_of_placeholder)
                        temp_more_curly = template_line.partition('{')[0].strip('\n\r')
                        
                        if temp_more_curly == '':
                            pass
                        else:
                            input_line = value_of_placeholder
                            value_of_placeholder = value_of_placeholder.partition(temp_more_curly)[0]
                            input_line = input_line.replace(value_of_placeholder, '')
   
                        # eg ['station', 'latitude'] or ['station', 'tags', 'key']
                        placeholder_var_in_list = match.strip("{}").split('.')
                        # remove 'station', ie first element
                        del placeholder_var_in_list[0]
                        # Now it should be either ['latitude'] or ['tags', 'key']
                        if placeholder_var_in_list[0] == 'tags':
                            station_dictionary['tags'][placeholder_var_in_list[-1]] = value_of_placeholder
                        else:
                            station_dictionary[placeholder_var_in_list[0]] = value_of_placeholder
        
        try:
            station_dictionary['tags'] = json.dumps(station_dictionary['tags'])
        except:
            pass
        station.update(station_dictionary)
    return station


def determine_if_file_is_csv_or_not(input_data: io.StringIO, template_data):
    """
    This function is based on a dummy assumption:
    If the count of `space` characters is bigger than the  count of `comma` characters in a document
    then it is not a csv.
    Following this, it transforms it using space_delimitted_to_csv
    :param input_data: input's data as a io.StringIO()
    :param template_data: template's data as a io.StringIO()
    :return: input_data, template_data (converted as csv or remained intact)
    """
    input_data.seek(0)
    input_text = input_data.read()
    if (input_text.count(' ') > input_text.count(',')) and input_text.count(',') < 10:
        # Change them!
        input_data = space_delimited_to_csv(input_file=input_data)
        input_data.seek(0)
        template_data = space_delimited_to_csv(input_file=template_data)
        template_data.seek(0)
    input_data.seek(0)
    return input_data, template_data


def parse_for_iterations(input_iteration_file, template_iteration_file, iterable_type='Station'):
    """
    I presume that files are formatted as csv.
    The strategy here is as follows:
    1. Clear anything that is not enclosed in {{}}. E.g. ":".
    TODO: Do the same for actual observations
    2. Create a dataframe from the csv file
    3. Change dataframe column names to the information derived from template. E.g. 1st column is station.station_id
    (strip "station.". !Attention .split('.')[-1])
    4. Drop any columns we don't want to really parse
    
    :param input_iteration_file:
    :param template_iteration_file:
    :param iterable_type: 'Station', 'Observables', 'Unit of Measurements'
    :return:
    """
    var_for_line = re.compile(r"{%for .*? in .*?%}\n(.*)\n{%endfor%}")
    var_name = re.compile(r"({{.*?}})")
    
    temp_iteration_file = template_iteration_file
    temp_iteration_file.seek(0)
    text = temp_iteration_file.read()
    
    # for_lines = "#{{station.station_id}}:,{{station.longtitude}},{{station.latitude}}"
    for_lines = re.findall(var_for_line, text)[0]
    # variables = ['{{station.station_id}}', '{{station.longtitude}}', '{{station.latitude}}']
    variables = [var for var in re.findall(var_name, for_lines)]
    
    characters_to_be_replaced = for_lines
    for variable in variables:
        characters_to_be_replaced = characters_to_be_replaced.replace(variable, '')
    # characters_to_be_replaced = "#:,,,,"
    # Thus we should remove comma character
    characters_to_be_replaced = characters_to_be_replaced.replace(',', '')
    for character_to_be_replaced in characters_to_be_replaced:
        for_lines = for_lines.replace(character_to_be_replaced, '')
    for_lines = for_lines.split(',')
    template_for_lines_indexed = dict(enumerate(for_lines))
    
    # Determine which indexes hold variables
    # Create dataframe header
    dataframe_header = []
    for counter_index in range(0, len(template_for_lines_indexed)):
        stripped_header = template_for_lines_indexed[counter_index].strip("{{}}")  # type: str
        stripped_header = stripped_header.split('.')
        # Remove station
        iterative_type = stripped_header[0]
        del stripped_header[0]
        # This is done for tags.something
        stripped_header = '.'.join(stripped_header)
        dataframe_header.append(stripped_header)
    
    df = pd.read_csv(input_iteration_file, na_values='', header=0, names=dataframe_header)
    
    for column in df.columns:
        # first strip
        try:
            df[column] = df[column].str.strip(to_strip=characters_to_be_replaced)
        except:
            pass
        if column.startswith('tags'):
            key = str(column.split('.')[-1])
            temp_dict = dict()
            temp_dict[key] = df[column].map(str)
            
            # Update column, key: value
            df[column] = "\"" + key + "\"" + ':' + "\"" + df[column].map(str) + "\""
            
            if 'tags' in df.columns:
                df['tags'] = df['tags'] + ',' + df[column]
            else:
                df['tags'] = '{' + df[column].map(str)
            # Drop this column
            df.drop(column, axis=1, inplace=True)
    # Exception will occur for observables for which we don't have tags
    try:
        df['tags'] = df['tags'] + '}'
        # df['tags'] = df['tags'].apply(lambda x: json.loads(x))
    except:
        pass
    
    # Station data(metadata) are stored directly to the database, while observables are sent back to
    # SourceConfiguration for further processing
    
    # just check the first column if 'observable' keyword is used.
    if iterative_type == 'observable':
        temp_iteration_file.seek(0)
        return df.to_dict(orient='index')
    
    else:
        data = DatabaseHandler()
        # Remove tags json field. It creates problems with pd.merge
        
        dup_cols = list(df)
        try:
            dup_cols.remove('tags')
        except:
            pass
        if database_type == "postgres":
            tablename = 'public."' + iterable_type + '"'
        elif database_type == "sqlite":
            tablename = '"' + iterable_type + '"'
        df_to_store = data.clean_df_db_dups(df=df, tablename=tablename, dup_cols=dup_cols)  # type: pd.DataFrame
        
        data.__add_dataframe__(dataframe=df_to_store, table=iterable_type, index=False, index_label=None)
        temp_iteration_file.seek(0)
        return [int(x) for x in df_to_store.index.tolist()]


def get_template_file_header_columns(template_file):
    """
    We sum the observables of a template
    :param template_file: 
    :return list:
    """
    template_file_text = template_file.read()
    template_file.seek(0)
    separator = "({.*?}+)"
    argument_list = list()
    
    # Each line is a list element
    lines = template_file_text.splitlines()
    
    # Remove empty lines
    [argument_list.append(remove_template_placeholders_from_string(line, separator)) for line in lines]
    argument_list = list(filter(str.strip, argument_list))
    return argument_list


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


def check_template_against_input_file(template_file: io.StringIO, data_input: io.StringIO):
    """
    We are going to work with every line (i.e. list element) individually.
    Specifically, we are going to check each of the lines against input files.
    If all lines match to a given input file, it means that we can parse data out of it.

    :param template_file: The name of the template (e.g. Yucheng.tmpl)
    :param data_input: Either data_input filename (e.g. Yucheng.met) or string with content stored in memory
    :param input_file_type: Either "File" or anything else (check data_input parameter)
    :return: True in case match is 100% or False in case match is NOT 100%
    """
    
    # utilities_logger.debug("Template: %s" % template_file.read())
    check_lines = get_template_file_header_columns(template_file=template_file)
    utilities_logger.debug("Check lines: %s" % check_lines)
    matching_percentage = int()
    
    utilities_logger.debug("Input file: %s" % data_input)
    
    input_lines = ''.join(list(itertools.islice(data_input, len(check_lines)))).strip('\n')
    
    for line in check_lines:
        
        if line in input_lines or line in input_lines.replace(' ', ''):
            matching_percentage += 1
    
    percentage = float(100 * matching_percentage / len(check_lines))
    if percentage > 20:
        return True
    else:
        return False


def get_template_for_vars(template_file):
    """
    This function parses:
    a. all templates located in /templates folder,
    b. the variables of each template in "for loop" (i.e. observable_id's)
    
    It then updates the database "Templates" table with all available templates.
    This function is useful for "viewing" purposes.
    A user can submit a query to the web portal and find all available templates along with the
    corresponding observable_id's
    
    :return:
    """
    for_loop_vars = re.compile(r"{%for (.*?) in .*?%}")
    
    text = template_file.read()
    match = re.search(for_loop_vars, text)
    if match:
        template_for_arguments = re.findall(for_loop_vars, text)[0]
        return template_for_arguments
    return None


def evaluate_variable_part(variable):
    """
    This function evaluates a variable (check parameter).
    :param variable:{0-n}
    :return: ['{0-n}': [0, 1, 2, ..., n]]
    """
    initial_var = copy.deepcopy(variable)
    variable = variable.strip('{}').split('-')
    if len(variable) > 2 or len(variable) < 2:
        utilities_logger.error(
            'Range %s is not correct in the correct format {starting_int - ending_int}' % initial_var)
        raise Exception('Range %s is not correct in the correct format {starting_int - ending_int}' % initial_var)
    
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
    except:
        utilities_logger.error("Can't convert variables to integers %s, %s" % (starting_number, ending_number))
        raise Exception("Can't convert variables to integers")
    
    the_range = range(starting_number, ending_number)
    # e.g. format(x,'02d')
    format_argument = '0' + str(length) + 'd'
    temp_list = [format(x, format_argument) for x in the_range]
    temp_as_a_dict = dict()
    temp_as_a_dict[initial_var] = temp_list
    
    return temp_as_a_dict


def generate_uri(uri: str(), static_variables=None):
    """
    This function generates a URI derivatives out of a URI which contains a variable part (i.e. {number-number})
    Variable parts are identified with regex.
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
    
    :param uri: URI with variable member as indicated by user (e.g. http://example.com/{01-09})
    :param static_variables:
    :return: A list with all resulting URIs. In case URI does not contain variable part (i.e. {01-09}),
    it returns one uri in a list
    """
    # variable_regex is more generic. It matches both {01-09} AND {$var} (i.e. static_variable_regex)
    variable_regex = r"({.*?})"
    static_variable_regex = r"({_var_})"
    match = re.search(variable_regex, uri)
    uris_in_a_list = list()
    if match:
        if re.search(static_variable_regex, uri):
            try:
                # We are in the case we have static variables
                static_variables_in_a_list = static_variables.split(',')
                for static_var in static_variables_in_a_list:
                    iteration_uri = copy.deepcopy(uri)
                    iteration_uri = iteration_uri.replace("{_var_}", static_var.strip())
                    uris_in_a_list.append(iteration_uri)
            except AttributeError:
                utilities_logger.error('--extra parameter was not given (Station variables). generate_uri()')
                raise AttributeError('--extra parameter (static vars) was empty')
        else:
            # We want all unique variable parts. See documentation about clusters!
            variable_parts_in_a_list = list(set(re.findall(variable_regex, uri)))
            evaluated_variable_parts = list(map(evaluate_variable_part, variable_parts_in_a_list))
            
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
                    iteration_uri = iteration_uri.replace(to_be_replaced[count], value)
                uris_in_a_list.append(iteration_uri)
    else:
        uris_in_a_list.append(uri)
    
    return uris_in_a_list


def download_and_check_with_tmpl_html_content_via_http(url: list(), template, template_object,
                                                       storage_type=StorageType.MEMORY):
    """
    This functions downloads and temporarily stores (in memory) html content of a given uri.
    Consequently, it checks if it matches against a given template (check parameter template).
    It the match is successful, html content is permanently stored in a file (in inputs/ folder).
    
    :param url:
    :param template:
    :param storage_type: Whether downloaded files to be stored in a file or in memory
    :return: (input_list, template)
    """
    input_list = list()
    template_name, _ = os.path.splitext(os.path.split(template)[1])
    
    # Create a folder to add downloaded files!
    if storage_type is StorageType.FILE:
        directory = os.path.join(home_directory, 'inputs', template_name)
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    for count, unique_url in enumerate(url):
        r = requests.get(unique_url)
        if r.status_code == 200:
            data_input = r.text
            if check_template_against_input_file(template_file=template_object, data_input=io.StringIO(data_input)):
                if storage_type is StorageType.FILE:
                    # Keep a backup!
                    file_type = r.headers['content-type']
                    file_encoding = None
                    if 'text/plain' in file_type:
                        file_encoding = ".txt"
                    elif 'text/html' in file_type:
                        file_encoding = ".html"
                    # elif "application/octet-stream" in file_type:
                    else:
                        # TODO: Fix this. It's like this to work for Bom!!!
                        file_encoding = ".txt"
                    filename = os.path.join(home_directory, 'inputs', template_name,
                                            template_name + str(count) + file_encoding)
                    with open(filename, 'w') as fp:
                        fp.write(data_input)
                
                input_list.append(io.StringIO(data_input))
        else:
            utilities_logger.warning(f"There is an error with: {unique_url}")
    
    return input_list, template


def check_if_path_exists(filename=None):
    """
    This utility function checks if a file exists.
    It first checks if the filename contains the path (e.g. ~/user/this/file.txt).
    If not it searches in the three folders located in user's home path (e.g. ~/.edam/inputs/, etc.)
    
    :param filename: The name of the file (e.g. Yucheng.met)
    :return: exists(True/False), filetype(Enum), FileObject (or None)
    """
    if os.path.exists(filename):
        # It means user gave full path
        # It may be a file or a folder
        if os.path.isfile(filename):
            return True, InputType.FILE, filename, open(filename, 'r')
        else:
            return True, InputType.FOLDER, filename, None
    else:
        # It means we have to find it
        for folder, included_folder, filenames in os.walk(home_directory):
            if '.viewer' in included_folder:
                included_folder.remove('.viewer')
            temp_path = os.path.join(folder, filename)
            
            if os.path.exists(temp_path):
                # It means user gave full path
                # It may be a file or a folder
                
                if os.path.isfile(temp_path):
                    return True, InputType.FILE, temp_path, open(temp_path, 'r')
                else:
                    return True, InputType.FOLDER, temp_path, None
        
        # If we are here it means that we couldn't find the file anywhere.
        # We should return False, None, None
        return False, None, None, None


def determine_storage_type(storage_as_string):
    """
    It transform string input ('file' or 'memory') to enum.StorageType
    :param storage_as_string: str: ('file' or 'memory')
    :return: enum.StorageType
    """
    try:
        return StorageType(storage_as_string)
    except:
        utilities_logger.error('Storage option should be \'file\' or \'memory\'. Not %s' % storage_as_string)
        raise SystemExit("Wrong storage option")


def identify_input_type(input_file: str, template, template_object, sql_query=None, extra_variables=None,
                        storage=StorageType.MEMORY):
    """
    This function identifies the type of given input and acts accordingly.
    Possible input type:
    - file
    - folder
    - http_url
    - database_connection string
    
    
    :return:
    """
    available_databases = ['postgres', 'sqlite', 'mysql', 'oracle']
    
    verified_inputs_as_list = []
    file_type = None
    if input_file.__contains__('http'):
        # We have a url!
        
        temp_inputs_as_list = generate_uri(uri=input_file, static_variables=extra_variables)
        
        verified_inputs_as_list, _ = download_and_check_with_tmpl_html_content_via_http(temp_inputs_as_list,
                                                                                        template=template,
                                                                                        template_object=template_object,
                                                                                        storage_type=storage)
        file_type = InputType.HTTP
    elif any(x in input_file for x in available_databases):
        # We have a database connection string
        # TODO: Check if database exists!
        db = records.Database(db_url=input_file)
        rows = db.query(sql_query)
        csv_name = home_directory + '/inputs/' + 'db_dump_' + str(int(datetime.now().timestamp())) + '.csv'
        with open(csv_name, 'w') as fp:
            fp.write(rows.export('csv'))
        if check_template_against_input_file(template_file=template, data_input=csv_name):
            verified_inputs_as_list.append(csv_name)
            file_type = InputType.DATABASE
        else:
            pass
    
    else:
        # We must have a file or a folder!
        exists, typ, input_file_path, _ = check_if_path_exists(input_file)
        if exists:
            if typ is InputType.FOLDER:
                # folder! Check if exists and iterate through all available files
                directory = input_file_path
                potential_files = list()
                for folder, included_folder, filenames in os.walk(directory):
                    for filename in filenames:
                        if not fnmatch.fnmatch(filename, '*.tmpl') and not fnmatch.fnmatch(filename, '.*'):
                            potential_files.append(open(os.path.join(folder, filename), 'r'))
                
                for potential_file in potential_files:
                    if check_template_against_input_file(template_file=template_object, data_input=potential_file):
                        verified_inputs_as_list.append(potential_file)
                        file_type = InputType.FILE
            
            else:
                # File
                # First we have to check if we can generate uris (e.g. files is "uk{01-90}.txt")
                # temp_list is either ['uk.txt'] (if input_file was "uk.txt") or
                # ['uk1.txt', 'uk2.txt', ..] (if input_file was "uk{01-90}.txt")
                temp_list = generate_uri(input_file_path, static_variables=extra_variables)
                for generated_file_uri in temp_list:
                    exists, file_type, path, file_object = check_if_path_exists(filename=generated_file_uri)
                    if exists and file_type is InputType.FILE:
                        # Let's check if we verify it with the template!
                        if check_template_against_input_file(template_file=template_object, data_input=file_object):
                            verified_inputs_as_list.append(file_object)
                            file_type = InputType.FILE
        else:
            raise SystemExit("%s does not exist" % input_file)
    if not verified_inputs_as_list:
        # It means we didn't find a single input to match with a template
        utilities_logger.warning("identify_input_type(): No verified inputs found")
        utilities_logger.info("No verified inputs found")
        return False, None, None
    else:
        return True, verified_inputs_as_list, file_type

if __name__ == "__main__":
    pass