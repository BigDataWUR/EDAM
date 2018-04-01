from edam.reader.models import Station

from edam.reader.utilities import find_and_describe_template


def check_template_source_compatibility(observable_id, station_object: Station):
    template_dictionary = find_and_describe_template(observable_id)
    print(observable_id)
    if template_dictionary:
        template_for_vars = template_dictionary['variables'].replace(' ', '').split(',')
    else:
        return False, None, False
    station_observable_ids = [helper.observable_id for helper in station_object.helper]
    station_observable_ids.append('timestamp')
    if set(template_for_vars) <= set(station_observable_ids):
        return True, template_for_vars, template_dictionary
    else:
        return False, None, None
