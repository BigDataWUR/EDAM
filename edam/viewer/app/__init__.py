import calendar
import hashlib
import os
import shutil
from datetime import datetime
from functools import wraps, update_wrapper

import jinja2
import pandas as pd
from flask import Flask, url_for, redirect
from flask import make_response
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

import edam.viewer.config as config
from edam.settings import home_directory
from edam.viewer.app.manage import DatabaseHandler as Data
from edam.viewer.app.manage import Measurement
from edam.viewer.app.utilities import check_template_source_compatibility


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            if "DS_" not in s:
                shutil.copy2(s, d)


app = Flask(__name__, static_folder=os.path.join(home_directory, '.viewer/', 'static'),
            static_url_path=os.path.join(home_directory, '.viewer/'))
app.config.from_object(config)

db = SQLAlchemy(app)

# Jinja trim whitespace
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Every time the server starts copy all user templates for viewing purposes
# TODO: It would be more efficient to create symlinks than hard-copying files
# copytree(os.path.join(home_directory, 'templates'),
#          os.path.join(home_directory, '.viewer', 'templates', 'edam'))

# Change the folder of templates and static files
app.jinja_loader = jinja2.FileSystemLoader([home_directory + '/.viewer/templates'])

# Don't sort with jsonify
app.config['JSON_SORT_KEYS'] = False

# Set cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

# secret key for sessions
app.secret_key = "this should be harder to guess"

data = Data()


@cache.cached(timeout=600, key_prefix='metastations')
def calculate_metastations():
    metastations = data.retrieve_stations()
    return metastations


@cache.cached(timeout=600, key_prefix='metatemplates')
def calculate_templates():
    metatemplates = data.retrieve_templates()
    return metatemplates


def calculate_data_and_render_from_template(observable_id, station_id):
    station_object = data.retrieve_object_from_id(table='Station', object_id=int(station_id))  # type: models.Station
    compatible, list_template_for_arguments, template_dictionary = check_template_source_compatibility(
        observable_id=observable_id,
        station_object=station_object)
    if compatible:
        station, chunk = data.retrieve_stations_data(station_object, list_template_for_arguments)
        return True, template_dictionary, station, chunk
    else:
        return False, redirect(url_for('index')), None, None


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


def flot(timestamp):
    return calendar.timegm(timestamp.timetuple()) * 1000


app.jinja_env.globals.update(flot=flot)


def hash(anything):
    return '_' + hashlib.md5(anything).hexdigest()


app.jinja_env.globals.update(hash=hash)


def d2s(datetime):
    return datetime.strftime("%D %H %M")


app.jinja_env.globals.update(d2s=d2s)


def same_timestamp(*args):
    if args:
        return args[0]
    else:
        return None


app.jinja_env.globals.update(same_timestamp=same_timestamp)


def resample(df: pd.DataFrame, rule, how=None, axis=0, fill_method=None, closed=None, label=None, convention='start',
             kind=None, loffset=None, limit=None, base=0, on=None, level=None):
    # observables_list = list(df)
    # pd.set_option('precision', 3)
    observables_list = ['timestamp', 'tmax', 'tmin', 'af', 'rain', 'sun']
    # observables_list = ['timestamp', 'radn', 'maxt', 'mint', 'rain', 'wind', 'RH']
    observables_list.remove('timestamp')
    available_operations = ['bfill', 'max', 'median', 'sum', 'min', 'interpolate', 'ffill']

    try:
        for observable in observables_list:
            df[observable] = df[observable].apply(lambda x: float(x))

    except Exception as e:
        print(e.args)
        print("I can't transform string value to float. Wind maybe? Check edam.viewer.__init__.py - downsample func")
        exit()
    resampled = df.resample("A", axis, fill_method, closed, label, convention, kind, loffset, limit, base, on,
                            level)

    resampled = resampled.mean()
    resampled = resampled.round(3)
    resampled = resampled.fillna('---')

    if how is None:
        if how in available_operations:
            # resampled = getattr(resampled, "interpolate")(method)
            resampled = getattr(resampled, how)()
    resampled["timestamp"] = resampled.index

    for observable in observables_list:
        resampled[observable] = resampled[observable].apply(lambda x: Measurement(x))
    # TODO: This is soooooo dangerous. Please re-implement......
    # observables_list.append('timestamp')
    observables_list = ['timestamp', 'tmax', 'tmin', 'af', 'rain', 'sun']
    # observables_list = ['timestamp', 'radn', 'maxt', 'mint', 'rain', 'wind', 'RH']
    zip_argument = map(lambda x: "resampled." + x, observables_list)

    zip_argument = ",".join(zip_argument)

    zip_argument = eval("zip(%s)" % zip_argument)

    return zip_argument


app.jinja_env.globals.update(resample=resample)

# def jsoni(uni):
#     return json.loads(uni, object_hook=json_util.object_hook)
# app.jinja_env.globals.update(jsoni = jsoni)
