import copy
import io
import logging
import re
from datetime import datetime

import numpy as np
import pandas as pd

from edam.reader.SourceConfiguration import SourceConfiguration
from edam.reader.manage import DatabaseHandler
from edam.reader.models import HelperTemplateIDs

var_name = re.compile(r"{{(.*?)}}")
var_for_loop = re.compile(r"{%\s?for (.*?) in (.*?)%}")
var_end_for_loop = re.compile(r"{%endfor%}")

# Above regex is for the case of same_timestamp(function) found in BoM template
var_same_timestamp = re.compile(r"(same_timestamp)\s?\((?P<args>(?P<arg>[\w.]+(,\s?)?)+)\)")

# This var corresponds to observables which value is located in more than one columns
# In our templating language they are represented as: {{observable.value[0]}},{{observable.value[1]}}, etc.
# With that regex we are going to determine the existence of those observables
var_multicolumn_values = re.compile(r"{{.*?\..*?(\[[0-9]\])*}}")

# For the following regex, line has to be splitted to ',' and then
# each individual var to be parsed with var_name
var_for_line = re.compile(r"{%\s?for .*? in .*?%}\n(.*)\n{%\s?endfor\s?%}")
var_parse_header = re.compile(r"(.*?)\n*{%\s?for .*? in .*?%}")

# var_anything_but_value = re.compile(r"{{.*?.value(.*?)}}")
# var_anything_but_value = re.compile(r"{{.+.value(\[.+\]).?.?}}")
var_for_value_timestamp = re.compile(r"{{.+.(timestamp.?)}}")

module_logger = logging.getLogger('edam.reader.TemplateReader')


def __determine_how_to_group_observables__(df_columns_indexed: dict):
    """
    This function determines how to parse observables. Some observables may have values and/or timestamps which
    expand in more than one columns. That function determines that and returns a list with indices.
    e.g. [1, 2, 3, 4, [5, 6, 7], 8, 9, [10, 11]]
    Above list means that 1, 2, 3, 4, 8, 9 should be parsed independently. 5,6,7 and 10,11 should be parsed
    as groups.
    In the returned list, if variable is "value" then index is of int type. If it's timestamp is of str type.
    E.g. In the list: [0, 1, 2, 3, 4, [5, 6, '7'], 8, 9, 10, [11, 12], 13, 14, 15, 16, [17, 18], 19]
    
    7 column contains timestamp.
    #TODO determine the type of timestamp.
    :param df_columns_indexed: Dictionary (index: value) (e.g. {0: '{{tmax.value}}', 1: '{{tmin.value}}', 2:
    '{{af.value}}', 3: '{{rain.value}}', 4: '{{sun.value}}'})

    :return:
    """
    
    how_to_parse = []
    temp = dict()
    args = list()
    for ind, var in df_columns_indexed.items():
        match_timestamp = re.search(var_for_value_timestamp, var)
        # match_multi_value = re.search(var_anything_but_value, var)
        index = copy.deepcopy(ind)
        # if match_timestamp or match_multi_value:
        argument = re.findall(var_name, var)[0]
        if match_timestamp:
        
            if "timestamp" in argument:
                index = str(index)
            
            argument = argument.strip(' \n\r').split('.')
            if len(argument) > 2:
                argument = argument[0] + argument[-1]
            else:
                argument = argument[0]
            
            args.append(argument)
            if argument not in temp.keys():
                temp[argument] = list()
            temp[argument].append(index)
        else:
            argument = argument.strip(' \n\r').split('.')[0]
            if argument in temp.keys():
                temp[argument].append(index)
            else:
                search_for = argument+".timestamp"
                if [s for s in df_columns_indexed.values() if search_for in s]:
                    temp[argument] = list()
                    temp[argument].append(index)
                else:
                    how_to_parse.append(index)
    while bool(temp):
        how_to_parse.append(temp.popitem()[1])

    return how_to_parse


def __get_statements_from_placeholders__(placeholder: str):
    return placeholder.split('=')


class TemplateReader:
    """
    This class takes 2 inputs:
    1. Source configuration object
    2. Connector object

    From those it infers:
    1. template
    2. input_file

    and exports:
    3. A list with observation objects, ready to be stored in the database.
    """
    
    def __init__(self, config=None, input_file=io.StringIO(),
                 template=io.StringIO()):
        self.template_logger = logging.getLogger('edam.reader.TemplateReader.TemplateReader')
        self.input_file = input_file
        self.template = template
        
        self.config = config
        
        self.Data = DatabaseHandler()
        
        self.df = None
        self.same_timestamp_arguments = None
        
        # I will create tuples (station,respective_dataframe,for_lines_indexed)
        # and append them in a list (parsing_tuples)
        # This process will be the first step. Parsing/storing and further processing follows.
        # station: The database id of the station for which data will be parsed
        # IMPORTANT: In case the input data is row-based and not column based
        # (i.e. australian data, see also git issue 6), we will generate a dataframe which will contain as many columns
        # as the "unique" observables of the station.
        
        # respective_dataframe: A dataframe which will have as index the timestamp column, and its related observables
        # will be located on the other df columns. Parsing/storing of such a df is already implemented.
        
        # for_lines_indexed: each dataframe should have its own for_line_indexed dictionary. Consider the example
        # of australian data. We have a number of station, each of which CAN POTENTIALLY have different observables..
        
        self.parsing_tuples = list()
        
        self.__open_template__()
        self.__set_dataframe_index_col()
        
        self.__create_dataframe_from_csv__()
        self.template_logger.info("I created the df from the csv")
        
        self.template_logger.info("I am starting handling stations")
        
        self.__handle_station_column__()
        self.template_logger.info("I am parsing data now")
        
        for station_id, station_respective_df, for_lines_indexed in self.parsing_tuples:
            self.template_logger.info("I am parsing station with %s id" % station_id)
            rows, columns = station_respective_df.shape
            self.template_logger.info("Rows: %d, Columns: %d" % (rows, columns))
            how_to_parse = __determine_how_to_group_observables__(df_columns_indexed=for_lines_indexed)
            self.__generate_pandas_series_from_df__(station_dataframe=station_respective_df,
                                                    how_to_parse=how_to_parse,
                                                    df_columns_indexed=for_lines_indexed,
                                                    station_id=station_id)
    
    def __open_template__(self):
        """
        This function open the self.template file and stores header (self.template_header_indexed) as dictionary
        and for_lines_arguments (self.template_for_lines_indexed) as dictionary.
        :return:
        """
        self.template.seek(0)
        text = self.template.read()
        # parse header
        header = re.findall(var_parse_header, text)[0].strip('\r\n').split(',')
        # create a dictionary with indices
        header = dict(enumerate(header))
        # TODO: Please check if the following is needed and remove.
        # self.template_header_indexed = dict(enumerate(header))
        
        # TODO: Please check if the following is needed and remove.
        for_lines = re.findall(var_for_line, text)[0].strip('\r\n').split(',{{')
        
        # for_lines = re.findall(var_for_line, text)[0].strip('\r\n')
        # for_lines = re.findall(var_name, for_lines)

        for_lines = list(map(lambda x: x if x.startswith("{{") else "{{" + x, for_lines))

        self.usecols = dict(enumerate(for_lines))
        self.usecols = list(filter(lambda key: re.search(var_name, self.usecols[key]), self.usecols))
        
        # Parse only values that need to be parsed (i.e. those inside placeholders{{}})
        for_lines = list(filter(lambda x: re.search(var_name, x), for_lines))
        
        self.template_for_lines_indexed = dict(enumerate(for_lines))
        self.for_lines = list(filter(lambda x: re.search(var_name, x), for_lines))
        self.for_lines = list(map(lambda x: x.strip("{}\r\n"), self.for_lines))
        self.template_header = dict()
        for index, label in self.template_for_lines_indexed.items():
            label_to_be_stored = label.strip("{}")
            if label_to_be_stored in self.template_header.keys():
                # TODO! This is so static, just to work for BoM! EDIT
                label_to_be_stored = label_to_be_stored + ".1"
            try:
                self.template_header[label_to_be_stored] = header[index]
            except Exception as e:
                self.template_logger.error(
                    "Can't create self.template_header for %s Exception: %s %s" % (
                        label_to_be_stored, type(e).__name__, str(e)))
        self.template.seek(0)
        
    def __set_dataframe_index_col(self):
        """
        This function creates a list with all values that will be passed over (self.no_parse_vars).
        It looks all for_line_vars, finds the one starts with "timestamp" and sets that column as the index of the
        dataframe.
        TODO: Make this more generic
        :return:
        """
        # In some cases timestamp could be extended in more than one columns
        # E.g. 09.05.2014,14:23:34,0.004
        # Thus index should be a dictionary: {date: index1, month: index2, time:index3}
        # Columns representing above indices should be merged when construction of dataframe takes place.
        self.parse_dates = dict()
        self.parse_dates['timestamp'] = dict()
        self.parse_dates['timestamp']['indices'] = list()
        self.parse_dates['timestamp']['format'] = list()
        self.index = {}
        for index, variable in self.template_for_lines_indexed.items():
            match = re.search(var_name, variable)
            match_same_timestamp = re.search(var_same_timestamp, variable)
            
            if match:
                if match_same_timestamp:
                    match_same_timestamp = re.search(var_same_timestamp, variable)
        
                    fn_dict = match_same_timestamp.groupdict()
                    arguments = [arg.strip() for arg in fn_dict['args'].split(',')]
                    # We pick one of the two, since they are the same
                    # argumemnts = ['windm_spd.timestamp.time', 'windm_dir.timestamp.time']
                    self.same_timestamp_arguments = arguments
                    name_of_variable_without_brackets = arguments[0]
                else:
                    name_of_variable_without_brackets = re.findall(var_name, variable)[0]
                    # name_of_variable_without_brackets: timestamp.date
                    # Thus splitting by '.' and taking the last item, ie. date, time, etc.
                    dict_key = name_of_variable_without_brackets.split('.')[-1]
                if name_of_variable_without_brackets.startswith("timestamp"):
                    self.parse_dates['timestamp']['indices'].append(index)
                    if dict_key.lower() == "year":
                        self.parse_dates['timestamp']['format'].append('%Y')
                    elif dict_key.lower() == "month":
                        self.parse_dates['timestamp']['format'].append('%m')
                    elif dict_key.lower() == "day":
                        self.parse_dates['timestamp']['format'].append('%d')
                    elif dict_key.lower() == "dayofyear":
                        self.parse_dates['timestamp']['format'].append('%j')
                    elif dict_key.lower() == "hour":
                        self.parse_dates['timestamp']['format'].append('%H')
                    elif dict_key.lower() == "minutes":
                        self.parse_dates['timestamp']['format'].append('%M')
                    elif dict_key.lower() == "seconds":
                        self.parse_dates['timestamp']['format'].append('%S')
                    else:
                        self.template_logger.debug("%s timestamp type" % dict_key)
                        pass
                elif "timestamp" in name_of_variable_without_brackets:
                    # all cases where timestamp is not first (e.g. wind.timestamp..)
                    additional_timestamp = name_of_variable_without_brackets.split('.')[0] + '.timestamp'
                    if additional_timestamp not in self.parse_dates:
                        self.parse_dates[additional_timestamp] = dict()
                        # All sub-timestamps depend on the main timestamp
                        self.parse_dates[additional_timestamp]['indices'] = copy.deepcopy(
                            self.parse_dates['timestamp']['indices'])
                    
                    self.parse_dates[additional_timestamp]['indices'].append(index)
    
    def __create_dataframe_from_csv__(self):
        """
        At the end of this function, df has as index the correct timestamp and has all non-relevant columns dropped.
        We still need to parse static information (such as timestamps) from the header, ie. the column names.
        :return:
        """
        # I don't parse the header of the input file. Instead I set the header to the template to be used for the
        # names of the df columns.
        if self.df is None:
            parse_dates = dict()
            for key, value in self.parse_dates.items():
                parse_dates[key] = value['indices']
            if self.parse_dates['timestamp']['format']:
                def date_parser(x):
                    try:
                        return datetime.strptime(x, ' '.join(self.parse_dates['timestamp']['format']))
                    except:
                        # This exception catches the case where in datetime column we have litter (e.g. Site closed)
                        return x
            else:
                date_parser = None
            self.df = pd.read_csv(self.input_file, na_values='---',
                                  header=0,
                                  usecols=self.usecols,
                                  names=self.for_lines,
                                  warn_bad_lines=True,
                                  parse_dates=parse_dates,
                                  date_parser=date_parser,
                                  infer_datetime_format=True,
                                  keep_date_col=False,
                                  error_bad_lines=False,)
            self.df.set_index(keys=["timestamp"], drop=True, inplace=True)
            # Drop nan rows and columns
            self.df.dropna(axis=0, how='all', inplace=True)
            self.df.dropna(axis=1, how='all', inplace=True)
            # Let's create duplicate lines of same_timestamp_arguments (if any)
            if self.same_timestamp_arguments:
                arguments = copy.deepcopy(self.same_timestamp_arguments)
                arguments = list(map(lambda x: x.split('.')[0] + '.timestamp', arguments))
                key_argument = copy.deepcopy(arguments[0])
                del arguments[0]
                # The following if clause is for bom data. When no windmax values are given...
                try:
                    check_list = list(filter(lambda x: 'nan' not in x, self.df[key_argument].values.tolist()))
                except:
                    check_list = True
                    
                if check_list:
                    for arg in arguments:
                        self.df[arg] = self.df[key_argument]
                else:
                    self.df.drop(key_argument, axis=1, inplace=True)
                
        else:
            pass

    def __handle_station_column__(self):
        temp_parsing_tuples = list()
        for key in list(self.template_for_lines_indexed):
            column_name = self.template_for_lines_indexed[key].strip('{{}}')
            
            # I assume that if station is mentioned in the observations iteration, it will be the FK to the station
            # to which the datapoints are referring to.
            # TODO: However, this should be more generic and predict any other unforeseen cases.
            if 'station' in column_name:
                distinct_stations = self.df[column_name].unique()
                
                for tags_station_id in distinct_stations:
                    # If the station is in the ones the users defined in their config file...
                    database_station_id = self.__return_dbstation_id_by_tags_value__(tags_station_id)
                    if database_station_id in self.config.station_id:
                        respective_station_df = self.df.loc[self.df[column_name] == tags_station_id].copy()
                        respective_station_df.drop(column_name, axis=1, inplace=True)
                        temp_parsing_tuples.append((database_station_id, respective_station_df))
                    else:
                        self.template_logger.warning("You are trying to parse station with database id '%s'. \n"
                                                     "However your input file does not contain "
                                                     "a station with this id. \n Program will exit shortly... \n" %
                                                     tags_station_id)
                
                self.template_for_lines_indexed.pop(key)
                break
        
        # Update template_for_line_indexed dictionary
        # This is an essential step since data parsing is based on this dictionary
        # Now let's check if we have the case of the australian data.
        # That is, if we have row-based data
        
        # if 'observable.observable_id' == column_name:
        #     unique_observables = self.df[column_name].unique()
        
        # I will now create a new df column for each of those unique observables.
        # The values of those
        
        temp_temp_parsing_tuples = list()
        
        if '{{observable.observable_id}}' in self.template_for_lines_indexed.values():
            for station, resp_df in temp_parsing_tuples:
                resp_df = resp_df.pivot_table(index=resp_df.index.name, columns='observable.observable_id',
                                              values='observable.observable_id.value')
                # resp_df = resp_df.pivot(columns='observable.observable_id', values='observable.observable_id.value')
                # try:
                #     resp_df = resp_df.pivot(columns='observable.observable_id', values='observable.observable_id.value')
                # except:
                #     print(resp_df)
                temp_temp_parsing_tuples.append((station, resp_df))
            del temp_parsing_tuples
            temp_parsing_tuples = temp_temp_parsing_tuples
        del temp_temp_parsing_tuples
        # If list is empty!
        if not temp_parsing_tuples:
            # I assume that in config one and only one station was defined..
            one_tuple = (self.config.station_id[0], self.df)
            temp_parsing_tuples.append(one_tuple)
            # self.parsing_tuples.append(one_tuple)
        
        # At this point we have dataframes which have timestamp as index, and other columns are for the observables
        for station_id, station_df in temp_parsing_tuples:
            temp_for_lines_indexed = dict()
            for column_name in list(station_df):
                # TODO: curly brackets are used for continuity purposes
                temp_for_lines_indexed[station_df.columns.get_loc(column_name)] = "{{" + column_name + "}}"
            tuple_to_be_added = station_id, station_df, temp_for_lines_indexed
            self.parsing_tuples.append(tuple_to_be_added)
    
    def __update_index_timestamp_from_column__(self, station_df, var, grouped_col=False):
        # Do something with only columns with additional timestamps
        # check if we need to parse data from header
        regex = re.compile(r'{%.?set (.*?).?%}')
        try:
            local_var = self.template_header[var]
        except Exception as e:
            self.template_logger.warning("%s %s" % (type(e).__name__, str(e)))
            self.template_logger.warning("I am returning df without updates")
            new_df = pd.DataFrame()
            new_df["value"] = pd.Series(station_df[var], index=station_df.index)
            return new_df
        match = re.search(regex, local_var)
        if grouped_col:
            new_df = station_df
        
        else:
            new_df = pd.DataFrame()
            new_df["value"] = pd.Series(station_df[var], index=station_df.index)
        if match:
            # example: {{wind.timestamp.hour=9}}
            fullname_in_list = re.findall(regex, local_var)[0]
            
            # example: ['wind.timestamp.hour', '9']
            splitted_by_equal_sign = __get_statements_from_placeholders__(fullname_in_list)
            
            # example: hour
            # but we need only the first letter
            # thus [0]
            unit = splitted_by_equal_sign[0].split('.')[-1][0]
            
            new_df.index += pd.TimedeltaIndex(pd.Series(np.full(new_df.shape[0],
                                                                int(splitted_by_equal_sign[1]))), unit=unit)
        
        return new_df
    
    def __determine_observable_id_from_db__(self, var, station_id) -> HelperTemplateIDs:
        """
        :param var: {{temp.value}}
        :return:
        """
        var = re.findall(var_name, var)[0].split('.')[0]
        helper_template_row = self.Data.__get_helper_table_row_input_file_observable_id__(var,
                                                                                        station_id)
        
        return helper_template_row
    
    def __generate_pandas_series_from_df__(self, station_dataframe, how_to_parse, df_columns_indexed, station_id):
        for col_index in how_to_parse:
            # if True it means the column should be parsed independently.
            # if False (list type), another for loop should be implemented
            # dataframe_to_store = pd.DataFrame()
            if type(col_index) is int:
                col_index = int(col_index)
                var = station_dataframe[station_dataframe.columns[col_index]].name
                dataframe_to_store = self.__update_index_timestamp_from_column__(station_df=station_dataframe,
                                                                                 var=var)  # type: pd.DataFrame()
                helper_id_row = self.__determine_observable_id_from_db__(df_columns_indexed[col_index], station_id)
                
                dataframe_to_store["helper_observable_id"] = pd.Series(helper_id_row.id, index=dataframe_to_store.index)
                
                update_helper_with_meta = dict()
                try:
                    update_helper_with_meta['frequency'] = pd.infer_freq(dataframe_to_store.index)
                    update_helper_with_meta['start_date'] = dataframe_to_store.index[0]
                    update_helper_with_meta['end_date'] = dataframe_to_store.index[-1]
                    update_helper_with_meta['number_of_observations'] = dataframe_to_store.__len__()
                    self.__update_helper_observable_id(helper_id_row, update_helper_with_meta)
                except:
                    pass
            else:
                dataframe_to_store = pd.DataFrame(index=station_dataframe.index)
                exits = False
                for grouped_column in col_index[:]:
                    if type(grouped_column) is str:
                        grouped_column = int(grouped_column)
                        
                        col_index.remove(str(grouped_column))
                        exits = True
                        break
                dataframe_to_store['value'] = station_dataframe.iloc[:, col_index].astype(str).apply(
                    lambda x: ' '.join(x),
                    axis=1)
                if exits and type(grouped_column) is int:
                    dataframe_to_store.index = station_dataframe[
                        station_dataframe[station_dataframe.columns[grouped_column]].name]
                
                # We don't care which col_index we will select. They are both referring to the same entity
                # They are grouped after all
                var = station_dataframe[station_dataframe.columns[col_index[0]]].name
                # Update index from column
                
                dataframe_to_store = self.__update_index_timestamp_from_column__(
                    station_df=dataframe_to_store, var=var, grouped_col=True
                )  # type: pd.DataFrame()
                
                helper_id_row = self.__determine_observable_id_from_db__(
                    df_columns_indexed[int(col_index[0])], station_id)
                dataframe_to_store["helper_observable_id"] = pd.Series(helper_id_row.id,
                                                                     index=dataframe_to_store.index)
                update_helper_with_meta = dict()
                try:
                    update_helper_with_meta['frequency'] = pd.infer_freq(dataframe_to_store.index)
                    update_helper_with_meta['start_date'] = dataframe_to_store.index[0]
                    update_helper_with_meta['end_date'] = dataframe_to_store.index[-1]
                    update_helper_with_meta['number_of_observations'] = dataframe_to_store.__len__()
                    self.__update_helper_observable_id(helper_id_row, update_helper_with_meta)
                except:
                    pass
            
            # Clean from duplicate records
            # dataframe_to_store = self.Data.clean_df_db_dups(df=dataframe_to_store, tablename="Observations",
            #                                                 dup_cols=list(dataframe_to_store))

            self.Data.__add_dataframe__(dataframe_to_store)
    
    def __check_if_observable_is_stored__(self, observable):
        return self.Data.__check_observable_is_in_db__(observable)
    
    def __return_dbstation_id_by_tags_value__(self, station_id):
        """
        #TODO: This function should be more generic. E.g. By placeholder value
        In the template we have something like: {{station.tags.station_id}}
        Logic of this program is "smart" enough to identify that station_id is a key of the JSON type "tag".
        Thus, this can be handled automatically in the future..
        :param station_id: tags station_id, e.g. 210
        :return: a dictionary. old_value:new_value
        """
        
        database_station_id = self.Data.__get_station_id_by_tags_station_id__(station_id)
        # for old_value, new_value in temp_dict.items():
        #     self.df[column_name] = self.df[column_name].replace(to_replace=old_value, value=new_value)
        return database_station_id
    
    def __check_if_sensor_is_stored__(self, sensor):
        """
        
        :param sensor:
        :return: True if it exists, False if it does not
        """
        return self.Data.__check_sensor_is_in_db__(sensor)
    
    def __store_item_in_db(self, item):
        self.Data.__add_item__(item)
    
    def __update_helper_observable_id(self, helper_observable_id: HelperTemplateIDs, meta_dictionary):
        # helper_observable_id.update_meta(metadata_in_dict=meta_dictionary)
        self.Data.__update_item__(helper_observable_id, metadata_dict=meta_dictionary)


if __name__ == "__main__":
    conf = SourceConfiguration(input_yaml="/Users/argyris/Documents/git/templateFramework/metadata/knmi.yaml",
                               input_file_data="/Users/argyris/Documents/git/templateFramework/inputs/knmi_alldata_data.txt")
    t = TemplateReader(config=conf,
                       input_file="/Users/argyris/Documents/git/templateFramework/inputs/knmi_alldata_data.txt",
                       template="/Users/argyris/Documents/git/templateFramework/templates/knmi_data.tmpl")
