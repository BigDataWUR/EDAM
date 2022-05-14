from edam.reader.models.measurement import Measurement
from edam import OGC_SOS_CONFIGURATION


class OgcSos:
    def __init__(self, request, procedure=None, offering=None,
                 event_time=None, observed_property=None, page=None):
        self.available_requests = [
            'GetCapabilities',
            'DescribeSensor',
            'GetObservation']
        self.offering = offering
        self.eventTime = event_time
        self.observedProperty = observed_property
        self.info = OGC_SOS_CONFIGURATION
        self.keywords = list()
        self.stations = list()
        self.results = list()
        self.metadata = list()
        self.procedure = procedure
        self.sensor = None
        self.page = page
        self.template = None

        self.exception = False
        self.helper_object = None

        self.exceptionDetails = {}

        self.data = None

        if request in self.available_requests:
            self.request = request
            self.determine_request()

    def determine_request(self):
        """
        Determines the type or request and sets the appropriate template
        """
        if self.request == "GetCapabilities":
            self.find_keywords()
            self.find_stations()
            self.find_metadata()
            self.template = "sos/GetCapabilities.xml"
        elif self.request == "DescribeSensor":
            # self.procedure is like: station_name:sensor_name:template_id

            try:
                station_id, sensor_id, template_id = self.procedure.split(':')
                exists = self.data.get_helper_for_describe_sensor(
                    station_id=station_id,
                    sensor_id=sensor_id,
                    template_id=template_id)
                if exists:

                    self.sensor = exists
                    self.template = "sos/DescribeSensor.xml"
                else:
                    self.template = "sos/DescribeSensorException.xml"
            except BaseException:
                self.template = "sos/DescribeSensorException.xml"
        elif self.request == "GetObservation":
            try:
                station_id, sensor_id, template_id = self.procedure.split(':')
                exists = self.data.get_helper_for_describe_sensor(
                    station_id=station_id, sensor_id=sensor_id,
                    template_id=template_id)
                if exists:
                    # from_time, to_time = self.eventTime.split('/')
                    # from_time = pd.to_datetime(from_time)
                    # to_time = pd.to_datetime(to_time)

                    self.helper_object = exists
                    results = self.data.get_observations_by_helper_id(
                        self.helper_object.id)
                    for row in results:
                        self.results.append(Measurement(value=row.value,
                                                        timestamp=row.timestamp,
                                                        observable=self.helper_object.observable,
                                                        uom=self.helper_object.uom,
                                                        station=self.helper_object.station,
                                                        helper=self.helper_object))
                    # self.results = [Measurement(value=row.value, timestamp=row.timestamp) for row in results]

                    self.template = "sos/GetObservation.xml"
                else:
                    self.template = "sos/GetObservationException.xml"
            except Exception as inst:
                print(inst)
                self.template = "sos/GetObservationException.xml"

    def find_keywords(self):
        [self.keywords.append(quantity.name)
         for quantity in self.data.get_all_observables()]

    def find_stations(self):
        [self.stations.append(station)
         for station in self.data.get_all_stations()]

    def find_metadata(self):
        [self.metadata.append(helper)
         for helper in self.data.get_all_helper_observable_ids()]
