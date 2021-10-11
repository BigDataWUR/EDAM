import os

import yaml
from sqlalchemy.engine.url import URL

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
home_directory = os.path.join(os.path.expanduser('~'), '.edam')
test_resources = os.path.join(ROOT_DIR, '../', 'tests', 'resources')
settings = os.path.join(home_directory, 'settings.yaml')

with open(settings, 'r') as stream:
    try:
        settings_content = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:
        raise exc


def safe_return(section, fields_as_dict):
    temp_dict = dict()
    for key, default_value in fields_as_dict.items():
        try:
            value = settings_content[section][key]
        except:
            value = default_value
        temp_dict[key] = value
    
    if section == 'DATABASE':
        if temp_dict['drivername'] in ['sqlite']:
            temp_dict['database'] = os.path.join(home_directory, temp_dict['database'])
    
    return temp_dict


database_fields = {'drivername': 'sqlite', 'database': 'edam.db'}
DATABASE = safe_return('DATABASE', database_fields)

server_fields = {'host': '127.0.0.1', 'port': '5000', 'debug': False}
SERVER = safe_return('SERVER', server_fields)
ogc_sos_fields = {'title': 'EDAM',
                  'description': 'EDAM OGC Sensor Observation Service',
                  'name': 'First name Last name',
                  'provider_name': 'Wageningen University',
                  'voice': '00302541-079-516',
                  'fax': '00302541-079-516',
                  'delivery_point': 'WUR',
                  'city': 'Wageningen',
                  'administration_area': 'Netherlands',
                  'postal_code': '',
                  'country': 'Netherlands'}

OGC_SOS_CONFIGURATION = safe_return('OGC SOS', ogc_sos_fields)
database_url = URL(**DATABASE)
database_type = DATABASE['drivername']

if __name__ == "__main__":
    print(test_resources)
