from edam.reader.models.station import Station
from edam.reader.models.template import Template


def template_matches_source(template: Template, station: Station):
    return True
    # if set(template_for_vars) <= set(station_observable_ids):
    #     return True, template_for_vars, template_dictionary
    # else:
    #     return False, None, None
