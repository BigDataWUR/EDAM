from edam.reader.models.station import Station
from edam.reader.models.template import Template


def template_matches_source(template: Template, station: Station):
    if set(station.observable_ids + ['timestamp']) >= set(
            template.observable_ids):
        return True
    return False
