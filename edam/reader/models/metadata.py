import os

import yaml

from edam.reader.database_handler import add_item
from edam.reader.models.observable import AbstractObservable
from edam.reader.models.sensor import Sensor
from edam.reader.models.station import Station
from edam.reader.models.unit_of_measurement import UnitOfMeasurement


class Metadata:
    def __init__(self, path=None):
        self.path = path

    @property
    def restructured_metadata(self):
        restr_meta = dict()
        observables = self.observables
        sensors = self.sensors
        unit = self.units_of_measurement
        for obs_id in self.observable_ids:
            restr_meta['station'] = self.station
            restr_meta[obs_id] = dict()
            restr_meta[obs_id]['sensor'] = sensors[obs_id]
            restr_meta[obs_id]['observable'] = observables[obs_id]
            restr_meta[obs_id]['unit_of_measurement'] = unit[obs_id]

        return restr_meta

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def contents(self):
        try:
            with open(self.path, 'r') as f:
                return yaml.load(f.read(), Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            return exc.args

    @property
    def observable_ids(self):
        return list(self.observables.keys())

    @property
    def station(self) -> Station:
        try:
            return self._station
        except AttributeError:
            return add_item(Station(**self.contents['Station']))

    @property
    def raw_station(self):
        return Station(**self.contents['Station'])

    @station.setter
    def station(self, value):
        self._station = add_item(value)

    @property
    def observables(self) -> [AbstractObservable]:
        return {item['observable_id']: add_item(AbstractObservable(**item))
                for item in self.contents['Observables']}

    @property
    def sensors(self):
        sensors = dict()
        if self.contents['Sensors'] is None:
            return sensors
        for sensor in self.contents['Sensors']:
            relevant_observables = map(
                lambda rel_obs: rel_obs.strip().lstrip().rstrip(),
                sensor.pop('relevant_observables').split(','))
            for observable_id in relevant_observables:
                sensor['abstract_observable_id'] = self.observables[
                    observable_id].id
                sensors[observable_id] = add_item(Sensor(**sensor))
        return sensors

    @property
    def units_of_measurement(self):
        unit = dict()
        for sensor in self.contents['Units of Measurement']:
            relevant_observables = map(
                lambda rel_obs: rel_obs.strip().lstrip().rstrip(),
                sensor.pop('relevant_observables').split(','))
            for observable_id in relevant_observables:
                unit[observable_id] = add_item(UnitOfMeasurement(**sensor))
        return unit
