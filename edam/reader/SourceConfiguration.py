import io
import os

import pandas as pd
import yaml
from geopy.geocoders import GoogleV3

from edam.reader.manage import DatabaseHandler
from edam.reader.models import Station, Sensors, AbstractObservables, UnitsOfMeasurement, \
    HelperTemplateIDs
from edam.reader.utilities import parse_for_iterations, extract_data_from_preamble, check_if_path_exists


def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


class SourceConfiguration:
    """
    This class handles configuration files, drafted by users.
    It reads it and extracts all relevant information.
    1. Creates the Station and Sensors objects. It checks if Station exists and appends related Sensors in it.
    2. Sets file locators for all corresponding input and output templates
    3. Sets locators for all corresponding inputs. Depending on the type (html, file, sql), calls the appropriate
    connector of the Connector class.
    
    A SourceConfiguration object serves as an input to TemplateReader.
    """
    
    def __init__(self, input_yaml, input_file_data=io.StringIO(), input_preamble=io.StringIO(),
                 template_preamble=io.StringIO()):
        """
        """
        # TODO: Implemenet this one..
        self.sensor_id = None
        
        self.database = DatabaseHandler()
        
        self.input_yaml = input_yaml
        self.input_file = input_file_data
        self.input_preamble = input_preamble
        self.template_preamble = template_preamble
        
        self.input_yaml.seek(0)
        self.input_file.seek(0)
        self.input_preamble.seek(0)
        self.template_preamble.seek(0)
        
        self.helper_template = pd.DataFrame(columns=['observable_id',
                                                     'abstract_observable_id',
                                                     'unit_id',
                                                     'station_id',
                                                     'sensor_id'])
        # self.available_fields = ['Station', 'Observables', 'Units of Measurement', 'Sensors', 'Data inputs']
        self.station_id = []
        self.content = None
        self.all_observable_ids = list()
        
        self.handler()
    
    def check_yaml(self):
        try:
            return yaml.load(self.input_yaml, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            return exc
    
    def handler(self):
        # Firstly we open the yaml
        self.content = self.check_yaml()
        
        # Check Station type
        station_type, source, template = self.__check_type_of_field(field_name='Station')
        
        if station_type == 'iterable':
            self.station_id = parse_for_iterations(input_iteration_file=source,
                                                   template_iteration_file=template, iterable_type='Station')
        else:
            self.set_station(parse_from_yaml=station_type)
        # Do the same for all other fields
        # Though this could be done only once.
        observable_type, source, template = self.__check_type_of_field(field_name='Observables')
        if observable_type == 'iterable':
            self.set_observables(iter_or_not=parse_for_iterations(input_iteration_file=source,
                                                                  template_iteration_file=template,
                                                                  iterable_type='Observables'))
        else:
            self.set_observables()
        
        # We should take care cases in which uom and sensor fields are empty.
        # If these fields are empty, it means that they should default to "unknown values"
        self.set_units_of_measurement()
        self.set_sensors()
        
        # Update dataframe. For some reason int is transformed to float. So here I revert this (for the affected columns
        self.helper_template['station_id'] = self.helper_template['station_id'].apply(int)
        self.helper_template['sensor_id'] = self.helper_template['sensor_id'].apply(int)
        self.helper_template['abstract_observable_id'] = self.helper_template['abstract_observable_id'].apply(int)
        self.helper_template['unit_id'] = self.helper_template['unit_id'].apply(int)
        
        # Now copy this dataframe so many times as the len(self.station_id)
        # self.helper_template = self.helper_template.append(temp, ignore_index=True)
        # We want to pass the first station_id since we already have this id incorporated.
        temp = self.helper_template.copy(deep=True)
        for station_id in self.station_id[1:]:
            temp['station_id'] = station_id
            self.helper_template = self.helper_template.append(temp, ignore_index=True)
        
        del temp
        # We have to check if we have duplicates!
        df_cleaned = self.database.clean_df_db_dups(df=self.helper_template, tablename='HelperTemplateIDs',
                                                    dup_cols=list(self.helper_template))
        
        self.database.__add_dataframe__(dataframe=df_cleaned, table='HelperTemplateIDs', index=False)
    
    def set_station(self, parse_from_yaml):
        """
        :return:
        """
        # With the following command I serialize a Station object from the .yaml file
        if parse_from_yaml is not None:
            station = Station.fromdictionary(self.content['Station'])  # type: Station
        else:
            station = Station()
        
        # It means metadata have to be parsed from the preambles
        if self.input_preamble.seek(0, os.SEEK_END) > 0 and self.template_preamble.seek(0, os.SEEK_END) > 0:
            self.input_preamble.seek(0)
            self.template_preamble.seek(0)
            station = extract_data_from_preamble(station, preamble_template=self.template_preamble
                                                 , preamble_input=self.input_preamble)
        
        # With the following command, I determine the existence of station object
        # with the same attributes (non-duplicate entries)
        
        exists, station_from_db = self.database.__check_station_is_in_db__(station)
        if exists:
            station_id = station_from_db.id
        else:
            station.latitude = safe_float(station.latitude)
            station.longitude = safe_float(station.longitude)
            if station.latitude is None and station.longitude is None and station.name is not None:
                geolocator = GoogleV3()
                try:
                    location = geolocator.geocode(station.name + station.region)
                except:
                    try:
                        location = geolocator.geocode(station.name)
                    except:
                        location = None
                if location is not None:
                    station.latitude = location.latitude
                    station.longitude = location.longitude
            
            _, station_id = self.database.__add_item__(station)
        
        self.station_id.append(station_id)
    
    def set_observables(self, iter_or_not=None):
        
        if iter_or_not is None:
            observables = self.content['Observables']
        else:
            observables = iter_or_not
            
            # This is where we should parse metadata of observables
            # parse_observables_with_reasoner(observables=observables)
        for obs in observables:
            observable_as_dict = obs  # type: dict
            # Deprecated
            # observable_as_dict['station_id'] = self.station_id
            observable = AbstractObservables.fromdictionary(observable_as_dict)
            exists, respective_abstract_observable_id = self.database.__check_observable_is_in_db__(observable)
            if exists:
                respective_abstract_observable_id = respective_abstract_observable_id[0]
            else:
                _, respective_abstract_observable_id = self.database.__add_item__(observable)
            
            # Create the 1/(len(station_id)) dataframe. The others would be exactly the same
            # apart the station_id section. This is derived of cedar requirements. I.e. Observables, uoms, sensors, etc
            # located in a config file regard ALL THE STATIONS in the config.
            
            temp = pd.Series({'observable_id': observable_as_dict['observable_id'],
                              'abstract_observable_id': respective_abstract_observable_id,
                              'unit_id': None,
                              'station_id': self.station_id[0],
                              'sensor_id': self.sensor_id
                              })
            
            self.all_observable_ids.append(observable_as_dict['observable_id'])
            
            self.helper_template = self.helper_template.append(temp, ignore_index=True)
    
    def set_helper_observable_ids(self, helper_template_as_dictionary):
        helperTemplateID = HelperTemplateIDs.fromdictionary(helper_template_as_dictionary)
        exists, _ = self.database.__chech_helperTemplateID_is_in_db__(helperTemplateID)
        if exists:
            pass
        else:
            _, _ = self.database.__add_item__(helperTemplateID)
    
    def set_units_of_measurement(self):
        
        if self.content['Units of Measurement'] is None:
            default_empty_uom = dict()
            default_empty_uom['name'] = "unknown"
            relevant_observables = self.all_observable_ids
            
            unit = UnitsOfMeasurement.fromdictionary(default_empty_uom)
            
            exists, unit_id = self.database.__check_unit_is_in_db__(unit)
            if exists:
                unit_id = unit_id[0]
            else:
                _, unit_id = self.database.__add_item__(unit)
            pass
            
            for observable_observable_id in relevant_observables:
                self.helper_template.loc[
                    self.helper_template['observable_id'] == observable_observable_id, 'unit_id'] = unit_id
        
        else:
            for uom in self.content['Units of Measurement']:
                uom_as_dict = uom  # type: dict
                if uom_as_dict['relevant_observables'] == '':
                    relevant_observables = self.all_observable_ids
                else:
                    relevant_observables = uom_as_dict['relevant_observables'].split(',')  # type: list
                    # remove spaces
                    relevant_observables = map(str.strip, relevant_observables)
                    # No need to keep it any more
                del uom_as_dict['relevant_observables']
                unit = UnitsOfMeasurement.fromdictionary(uom_as_dict)
                
                exists, unit_id = self.database.__check_unit_is_in_db__(unit)
                if exists:
                    unit_id = unit_id[0]
                else:
                    _, unit_id = self.database.__add_item__(unit)
                
                for observable_observable_id in relevant_observables:
                    self.helper_template.loc[
                        self.helper_template['observable_id'] == observable_observable_id, 'unit_id'] = unit_id
    
    def set_sensors(self):
        """
        :return:
        """
        if self.content['Sensors'] is None:
            default_empty_sensor = dict()
            default_empty_sensor['generic'] = True
            
            relevant_observables = self.all_observable_ids
            for observable_observable_id in relevant_observables:
                sensor = Sensors.fromdictionary(default_empty_sensor)
                # abstract_observable_id = None or id
                abstract_observable_id = \
                    self.helper_template.loc[(self.helper_template['station_id'] == self.station_id[0]) &
                                             (self.helper_template['observable_id'] == observable_observable_id)][
                        'abstract_observable_id'].values[0]
                abstract_observable_id = int(abstract_observable_id)
                
                unit_id = \
                    self.helper_template.loc[(self.helper_template['station_id'] == self.station_id[0]) &
                                             (self.helper_template['observable_id'] == observable_observable_id)][
                        'unit_id'].values[0]
                unit_id = int(unit_id)
                
                default_empty_sensor['unit_id'] = unit_id
                default_empty_sensor['abstract_observable_id'] = abstract_observable_id
                sensor.update(default_empty_sensor)
                
                exists, sensor_id = self.database.__check_sensor_is_in_db__(sensor)
                
                if exists:
                    sensor_id = sensor_id[0]
                else:
                    _, sensor_id = self.database.__add_item__(sensor)
                
                # We now need to update helper template ids table
                self.helper_template.loc[
                    (self.helper_template['station_id'] == self.station_id[0]) &
                    (self.helper_template['observable_id'] == observable_observable_id), 'sensor_id'] = sensor_id
        
        else:
            
            for sensor in self.content['Sensors']:
                sensor_as_dict = sensor  # type: dict
                if sensor_as_dict['relevant_observables'] == '':
                    relevant_observables = self.all_observable_ids
                else:
                    relevant_observables = sensor_as_dict['relevant_observables'].split(',')  # type: list
                    relevant_observables = map(str.strip, relevant_observables)
                    # No need to keep it any more
                # No need to keep it any more
                del sensor_as_dict['relevant_observables']
                # We have to retrieve abstract_observable_id from observable_id
                # We are going to do this, through the HelperTemplateIDs
                # After retrieving this id, we will update 'sensor' object, check if it's in db already
                # And finally store it.
                
                # A generic sensor can have more than one relevant_observables
                # In this case, we are going to create as many generic sensor objects as the relevant_observables..
                
                # We are going to determine the observable_id through the observable_id
                
                for observable_observable_id in relevant_observables:
                    sensor = Sensors.fromdictionary(sensor_as_dict)
                    # abstract_observable_id = None or id
                    abstract_observable_id = \
                        self.helper_template.loc[(self.helper_template['station_id'] == self.station_id[0]) &
                                                 (self.helper_template['observable_id'] == observable_observable_id)][
                            'abstract_observable_id'].values[0]
                    abstract_observable_id = int(abstract_observable_id)
                    
                    unit_id = \
                        self.helper_template.loc[(self.helper_template['station_id'] == self.station_id[0]) &
                                                 (self.helper_template['observable_id'] == observable_observable_id)][
                            'unit_id'].values[0]
                    unit_id = int(unit_id)
                    
                    sensor_as_dict['unit_id'] = unit_id
                    sensor_as_dict['abstract_observable_id'] = abstract_observable_id
                    sensor.update(sensor_as_dict)
                    sensor.generic = True
                    exists, sensor_id = self.database.__check_sensor_is_in_db__(sensor)
                    # Next line is resolving a bug introduced by sqlite
                    # For some unknown reason a str type was interpreted as dict when it came for storing
                    sensor.tags = str(sensor.tags)
                    if exists:
                        sensor_id = sensor_id[0]
                    else:
                        _, sensor_id = self.database.__add_item__(sensor)
                    
                    # We now need to update helper template ids table
                    self.helper_template.loc[
                        (self.helper_template['station_id'] == self.station_id[0]) &
                        (self.helper_template['observable_id'] == observable_observable_id), 'sensor_id'] = sensor_id
    
    def __check_type_of_field(self, field_name):
        """
        This function checks each given field values and determines the "type" of values.
        These could be in the form of "source:..., template:...", which means we need to
        iterate through source file and extract the fields. The other type is where fields
        are manually iterated in the config file, in the form of 1..., 2..., 3...
        :return: source_type (iterable, non_iterable), source (source_path, None), template (template_path, None)
        """
        # If True it means we have to extract data from iterable.
        try:
            if ('source' and 'template') in self.content[field_name]:
                source_type = 'iterable'
                source = self.content[field_name]['source']
                template = self.content[field_name]['template']
                sexists, _, sourcef, source_io_object = check_if_path_exists(source)
                texists, _, templatef, template_io_object = check_if_path_exists(template)
                
                if sexists and texists:
                    pass
                else:
                    # TODO logging!
                    raise SystemExit("%s and %s does not exist" % (source, template))
            
            else:
                source_type = 'non_iterable'
                source_io_object = io.StringIO()
                template_io_object = io.StringIO()
            
            return source_type, source_io_object, template_io_object
        except KeyError:
            # It means that yaml does not contain this field (e.g. Station, or Observable).
            # That is because metadata are PROBABLY stored in input files (preamble)
            return None, None, None


if __name__ == "__main__":
    test = SourceConfiguration('metadata/knmi.yaml', 'inputs/Yucheng.csv')
