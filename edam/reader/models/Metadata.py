import os

import yaml

from edam.reader.models.AbstractObservable import AbstractObservable
from edam.reader.models.UnitOfMeasurement import UnitOfMeasurement
from edam.reader.models.Sensor import Sensor
from edam.reader.models.Station import Station


class Metadata:
    def __init__(self, path=None):
        self.path = path

    @property
    def restructured_metadata(self):
        restructured_metadata = dict()
        sensors = self.sensors
        observables = self.observables
        units_of_measurement = self.units_of_measurement
        for observable_id in self.observable_ids:
            restructured_metadata['station'] = self.station
            restructured_metadata[observable_id] = dict()
            restructured_metadata[observable_id]['sensor'] = sensors[observable_id]
            restructured_metadata[observable_id]['observable'] = observables[observable_id]
            restructured_metadata[observable_id]['unit_of_measurement'] = units_of_measurement[observable_id]

        return restructured_metadata

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
            return Station(**self.contents['Station'])

    @station.setter
    def station(self, value):
        self._station = value

    @property
    def observables(self) -> [AbstractObservable]:
        return {item.pop('observable_id'): AbstractObservable(**item) for item in self.contents['Observables']}

    @property
    def sensors(self):
        sensors = dict()
        if self.contents['Sensors'] is None:
            return sensors
        for sensor in self.contents['Sensors']:
            relevant_observables = map(lambda rel_obs: rel_obs.strip().lstrip().rstrip(),
                                       sensor.pop('relevant_observables').split(','))
            for observable_id in relevant_observables:
                sensors[observable_id] = Sensor(**sensor)
        return sensors

    @property
    def units_of_measurement(self):
        units_of_measurement = dict()
        for sensor in self.contents['Units of Measurement']:
            relevant_observables = map(lambda rel_obs: rel_obs.strip().lstrip().rstrip(),
                                       sensor.pop('relevant_observables').split(','))
            for observable_id in relevant_observables:
                units_of_measurement[observable_id] = UnitOfMeasurement(**sensor)
        return units_of_measurement
