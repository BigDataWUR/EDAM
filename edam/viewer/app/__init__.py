import hashlib
import os
from datetime import datetime
from functools import wraps, update_wrapper

import jinja2
from flask import Flask
from flask import make_response
from flask_sqlalchemy import SQLAlchemy

from edam import get_logger
from edam.reader.database_handler import get_all
from edam import home_directory
from edam.reader.models.template import find_templates_in_directory
from edam.viewer import config
from edam.viewer.app.utilities import template_matches_source

# These are needed despite not all being used
from edam.reader.models.station import Station
from edam.reader.models.junction import Junction
from edam.reader.models.template import Template
from edam.reader.models.unit_of_measurement import UnitOfMeasurement
from edam.reader.models.observable import AbstractObservable
from edam.reader.models.sensor import Sensor

logger = get_logger('edam.viewer.app')

app = Flask(__name__,
            static_folder=os.path.join(home_directory, '.viewer/', 'static'),
            static_url_path=os.path.join(home_directory, '.viewer/'))
app.config.from_object(config)

db = SQLAlchemy(app)

# Jinja trim whitespace
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Change the folder of templates and static files
app.jinja_loader = jinja2.FileSystemLoader(
    [home_directory + '/.viewer/templates'])

# Don't sort with jsonify
app.config['JSON_SORT_KEYS'] = False

# secret key for sessions
app.secret_key = "this should be harder to guess"


def stations():
    all_stations = get_all(Station)
    return all_stations


def templates():
    all_templates = find_templates_in_directory()
    return all_templates


def render_data(template, station):
    if template_matches_source(template=template, station=station):
        return station.data_iter(template)
    else:
        return None


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers[
            'Cache-Control'] = 'no-store, no-cache, must-revalidate, ' \
                               'post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


def hash(anything):
    return '_' + hashlib.md5(anything).hexdigest()


app.jinja_env.globals.update(hash=hash)


def d2s(datetime_object):
    return datetime_object.strftime("%D %H %M")


app.jinja_env.globals.update(d2s=d2s)


def same_timestamp(*args):
    if args:
        return args[0]
    else:
        return None


app.jinja_env.globals.update(same_timestamp=same_timestamp)
