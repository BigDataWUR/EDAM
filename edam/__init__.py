import logging
import sys
from logging.handlers import TimedRotatingFileHandler
import os

import yaml
from sqlalchemy.engine.url import URL

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
home_directory = os.path.join(os.path.expanduser('~'), '.edam')
test_resources = os.path.join(ROOT_DIR, os.pardir, 'tests', 'resources')
settings = os.path.join(home_directory, 'settings.yaml')

with open(settings, 'r') as stream:
    try:
        settings_content = yaml.load(stream, Loader=yaml.BaseLoader)
    except yaml.YAMLError as exc:
        raise exc


def safe_return(section: str, fields: dict) -> dict:
    """
    :param section:
    :param fields:
    :return:
    """
    temp_dict = dict()
    for key, default_value in fields.items():
        try:
            value = settings_content[section][key]
        except KeyError:
            value = default_value
        temp_dict[key] = value

    if section == 'DATABASE':
        if temp_dict['drivername'] in ['sqlite']:
            temp_dict['database'] = os.path.join(
                home_directory, temp_dict['database'])

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
database_url = URL.create(**DATABASE)
database_type = DATABASE['drivername']

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = os.path.join(os.path.expanduser('~'), '.edam', "edam.log")
log_level = safe_return('GENERAL', {'loglevel': 'INFO'})
log_level = logging.getLevelName(log_level['loglevel'].upper())


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger
