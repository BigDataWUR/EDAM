from edam.reader.models.Station import Station
from edam.reader.models.Template import Template


def check_template_source_compatibility(template: Template, station: Station):
    if template_dictionary:
        template_for_vars = template_dictionary['variables'].replace(
            ' ', '').split(',')
    else:
        return False, None, False
    station_observable_ids = [
        helper.observable_id for helper in station.helper]
    station_observable_ids.append('timestamp')
    if set(template_for_vars) <= set(station_observable_ids):
        return True, template_for_vars, template_dictionary
    else:
        return False, None, None
