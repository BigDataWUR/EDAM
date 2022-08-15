import datetime

from flask import render_template

from edam.reader.models.measurement import Measurement
from edam import OGC_SOS_CONFIGURATION


class OgcSos:
    def __init__(self, stations=None):

        self.stations = stations
        self.info = OGC_SOS_CONFIGURATION
        self.keywords = [f"{station.name}:{junction.observable.name}" for
                         station in stations for junction in station.junctions]

    def resolve_request(self, request=None, **kwargs):
        """
        Determines the type or request and sets the appropriate template
        """
        if request is None:
            return
        if request == "GetCapabilities":
            return self.get_capabilities(**kwargs)
        elif request == "DescribeSensor":
            return self.describe_sensor(**kwargs)
        elif request == "GetObservation":
            return self.get_observation(**kwargs)

    def get_capabilities(self, **kwargs):
        template = "sos/GetCapabilities.xml"
        template_related = {
            "template_name_or_list": template,
            "info": self.info,
            "keywords": self.keywords,
            "stations": self.stations
        }
        return template_related

    def describe_sensor(self, **kwargs):

        procedure = kwargs['procedure']
        station_name, sensor_name = procedure.split(':')
        station = filter(lambda st: st.name == station_name, self.stations)
        try:
            station = next(station)
        except StopIteration:
            template_related = {
                "template_name_or_list": "sos/DescribeSensorException.xml",
                "exception_text": f"*{procedure}* does not exist. "
                                  f"*{station_name}* is not a station.",
            }
            return template_related
        junction = filter(lambda sen: sen.sensor.name == sensor_name,
                          station.junctions)
        try:
            junction = next(junction)
        except StopIteration:
            template_related = {
                "template_name_or_list": "sos/DescribeSensorException.xml",
                "exception_text": f"*{procedure}* does not exist. "
                                  f"*{sensor_name}* is not a sensor name.",
            }
            return template_related

        template_related = {
            "template_name_or_list": "sos/DescribeSensor.xml",
            "station": station,
            "junction": junction,
        }
        return template_related

    def get_observation(self, **kwargs):
        offering = kwargs['offering']
        station_name = offering
        station = filter(lambda st: st.name == station_name, self.stations)
        try:
            station = next(station)
        except StopIteration:
            template_related = {
                "template_name_or_list": "sos/GetObservationException.xml",
                "exception_text": f"*{station_name}* station does not exist."
            }
            return template_related
        observed_property = kwargs['observed_property']
        if observed_property is None:
            template_related = {
                "template_name_or_list": "sos/GetObservationException.xml",
                "exception_text": f"observedProperty does not exist. "
            }
            return template_related
        else:
            junction = filter(
                lambda sen: sen.observable.observable_id == observed_property,
                station.junctions)
            try:
                junction = next(junction)
            except StopIteration:
                template_related = {
                    "template_name_or_list": "sos/GetObservationException.xml",
                    "exception_text": f"*{observed_property}* observed property"
                                      f" does not exist."
                }
                return template_related

            # observed_property exists
            event_time = kwargs['event_time']
            if event_time:

                start, end = event_time.split('/')
                try:
                    start_date = datetime.datetime.strptime(start,
                                                            "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    start_exists = False
                else:
                    start_exists = True
                try:
                    end_date = datetime.datetime.strptime(end,
                                                          "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    end_exists = False
                else:
                    end_exists = True

                if start_exists and end_exists:
                    raw = station.data.loc[lambda df: df.index >= start_date and df.index <= end_date,:]
                elif start_exists and not end_exists:
                    raw = station.data.loc[lambda df: df.index >= start_date, :]
                elif not start_exists and end_exists:
                    raw = station.data.loc[lambda df: df.index <= end_date, :]

                raw = raw[observed_property]
                raw = raw.to_dict()
            else:
                raw = station.data[observed_property].to_dict()

            measurements = list()

            for timestamp, value in raw.items():
                measurements.append(
                    Measurement(timestamp=timestamp, value=value))

            template_related = {
                "template_name_or_list": "sos/GetObservation.xml",
                "junction": junction,
                "station": station,
                "measurements": measurements
            }
            return template_related
