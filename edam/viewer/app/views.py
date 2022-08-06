import json
import os.path

from flask import render_template
from flask import request, make_response, jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

import plotly
import plotly.graph_objs as go

from edam import get_logger
from edam.reader.models.station import Station
from edam.reader.models.template import Template
from edam.utilities.exceptions import InvalidUsage
from edam.viewer.app import app, stations, nocache, templates, \
    render_data
from edam.viewer.app.OgcSos import OgcSos

logger = get_logger('edam.viewer.app.views')

GoogleMaps(app)


@app.route('/maps/')
@app.route('/index/')
@app.route('/')
def mapview():
    markers = list()
    for station in stations():
        if station.latitude is not None and station.longitude is not None:
            observables = ', '.join(
                [junction.observable.name for junction in station.junctions])

            infobox = f'<p><b>Station</b>: ' \
                      f'<a href="{request.url_root}Stations/{station.id}" ' \
                      f'target="_blank">{station.name}</a></p>' \
                      f'<p><b>Observables</b>: {observables}</p>'
            temp_dict = {
                'lat': station.latitude,
                'lng': station.longitude,
                'infobox': infobox}
            markers.append(temp_dict)
    mymap = Map(
        identifier="map-canvas",
        lat=38.045362,
        lng=23.715078,
        zoom=3,
        markers=markers,
        style="width:100%;height:650px;"
    )
    return render_template('maps.html', mymap=mymap)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return render_template('error.html', errorTitle=str(
        error.status_code), errorMessage=error.message)


@app.route('/Stations')
@app.route('/Stations/')
@app.route('/stations')
@app.route('/stations/')
def stat():
    stations_dict = {station.id: station.as_dict() for station in stations()}
    return stations_dict


@app.route('/home')
@app.route('/home/')
def index():
    return render_template('home.html')


@app.route('/Stations/<station>')
@app.route('/stations/<station>')
def specific_station(station):
    stations_dict = {station.id: station.as_dict() for station in stations()}
    return jsonify(stations_dict[int(station)])


@app.route('/templates')
@app.route('/templates/')
def templ():
    templates_dict = {template.name: template.to_dict() for template in
                      templates()}
    return templates_dict


@app.route('/templates/<template>')
def specific_template(template):
    try:
        temp = next(filter(lambda item: item.name == template, templates()))

        response = make_response(temp.contents)
        response.headers['Content-type'] = 'text/plain'
        return response
    except StopIteration:
        raise InvalidUsage(
            f'{template} template does not exist', status_code=410)


@app.route('/data')
@nocache
def get_data():
    station_name = request.args.get('station')
    template_name = request.args.get('template')
    try:
        station = next(filter(lambda item: item.name == station_name,
                              stations()))  # type: Station
    except StopIteration:
        message = f"Station {station_name} does not exist"
        logger.warn(message)
        raise InvalidUsage(message, status_code=410)
    try:
        template = next(
            filter(lambda item: item.name == template_name,
                   templates()))  # type: Template
    except StopIteration:
        message = f"Template {template_name} does not exist"
        logger.warn(message)
        raise InvalidUsage(message, status_code=410)

    data = render_data(template=template,
                       station=station)
    if data is not None:
        if template.resampled:
            station.res = data
            response = make_response(
                render_template(os.path.join('edam', template.filename),
                                station=station))
        else:
            response = make_response(
                render_template(os.path.join('edam', template.filename),
                                chunk=data,
                                station=station))
        response.headers['Content-type'] = 'text/plain'
        response.headers['Cache-Control'] = 'public, max-age=0'

        return response
    else:
        raise InvalidUsage(
            f'{template_name} template and {station.name} station '
            f'are not compatible',
            status_code=410)


@app.route('/about/')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/graphs')
def graphs():
    all_stations = stations()  # type: [Station]
    return render_template('graphs.html', stations=all_stations)


@app.route('/line', methods=['GET', 'POST'])
def line_graph():
    metrics = request.args['metrics'].split(',')
    st = request.args['stations'].split(',')
    graph_json = line_plotter(metrics, st)
    data_to_return = dict()
    data_to_return['data_json'] = graph_json
    data_to_return['layout'] = dict()
    data_to_return['layout']['title'] = f"{','.join(metrics)}"

    return data_to_return


@app.route('/_get_metrics')
def station_metrics():
    station = request.args.get('station', 'none')
    try:
        station = next(filter(lambda sts: sts.name == station, stations()))

        return [dict(metric=metric) for metric in station.observable_ids]
    except StopIteration:
        return []


def line_plotter(metrics, st):
    tracers = list()
    for sta in st:
        try:
            station = next(filter(lambda sts: sts.name == sta, stations()))
        except StopIteration:
            return {}
        for metric in metrics:
            df = station.data
            metric_formal = next(
                filter(lambda it: it.observable.observable_id == metric,
                       station.junctions))

            trace = go.Scatter(
                x=df.index,
                y=df[metric],
                mode='lines',
                name=f'{station.name} - '
                     f'{metric_formal.observable.name.capitalize()}'
            )
            tracers.append(trace)
    graph_json = json.dumps(tracers, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json


@app.route('/SensorObservationService/')
def sensor_info():
    return render_template('SOS_Examples.html')


@app.route('/sos/')
@app.route('/Sos/')
@app.route('/sos/')
@app.route('/SOS/')
def sos():
    sos_request = request.args.get('request', '')
    sos_procedure = request.args.get('procedure', '')
    sos_offering = request.args.get('offering', '')
    sos_observed_property = request.args.get('observedProperty', '')
    sos_event_time = request.args.get('eventTime', '')

    sos = OgcSos(
        sos_request,
        sos_procedure,
        sos_offering,
        sos_event_time,
        sos_observed_property)
    sos_response = sos

    response = make_response(
        render_template(
            sos_response.template,
            info=sos.info,
            keywords=sos.keywords,
            stations=sos.stations,
            helpers=sos.metadata,
            procedure=sos.procedure,
            sensor=sos.sensor,
            results=sos.results,
            helper=sos.helper_object))
    response.headers["Content-Type"] = "application/xml"

    return response


if __name__ == "__main__":
    pass
