import copy
import json
from typing import TYPE_CHECKING

import pandas as pd

from edam.reader.database_handler import update_object, exists

if TYPE_CHECKING:
    from edam.reader.models.template import Template
    from edam.reader.models.station import Station


def resample(station: "Station", rule, how=None):
    dataframe = station.data
    rule = rule.lstrip('"').lstrip("'").rstrip('"').rstrip("'")
    observables_list = list(dataframe)
    observables_list.remove('timestamp')
    available_operations = [
        'bfill',
        'max',
        'median',
        'sum',
        'min',
        'interpolate',
        'ffill',
        'mean']

    try:
        for observable in observables_list:
            dataframe[observable] = dataframe[observable].apply(
                lambda x: float(x))

    except Exception as e:
        # logger.exception("Exception")
        pass
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])
    resampled = dataframe.resample(rule=rule, on='timestamp')

    if how is None:
        resampled = resampled.mean()
        resampled = resampled.round(3)
        resampled = resampled.fillna('---')
    else:
        how = how.lstrip('"').lstrip("'").rstrip('"').rstrip("'")
        if how in available_operations:
            resampled = getattr(resampled, how)()
            resampled = resampled.round(3)

    resampled['timestamp'] = resampled.index
    for observable in list(resampled):
        resampled[observable] = resampled[observable].apply(
            lambda x: str(x))
    return resampled


def update_existing(obj, new_values, logger):
    for key, value in new_values.items():
        try:
            if key in ['tags', 'qualifiers']:
                temp = getattr(obj, key)  # type: dict
                try:
                    value.update(temp)
                except ValueError as exception:
                    logger.warning(f"{exception}")
            setattr(obj, key, value)
        except AttributeError:
            logger.warning(f"{key} does not exist")
    if exists(obj) is None:
        update_object(obj)


def as_dict(obj):
    temp_dict = copy.deepcopy(obj.__dict__)  # type: dict
    temp_dict.pop("_sa_instance_state")
    for key in list(temp_dict.keys()):
        if key.startswith('_'):
            temp_dict[key.lstrip('_')] = json.loads(temp_dict[key])
            temp_dict.pop(key)

    return temp_dict
