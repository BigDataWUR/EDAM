from flask import render_template
from flask import request, make_response, jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

from edam.utilities.exceptions import InvalidUsage
from edam.viewer.app import app, stations, nocache, templates, \
    calculate_data_and_render_from_template
from edam.viewer.app.OgcSos import OgcSos

GoogleMaps(app)


@app.route('/maps/')
@app.route('/index/')
@app.route('/')
def mapview():
    metastations = stations()
    markers = list()
    for station in metastations:
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


@app.route('/home/')
def index():
    return render_template('home.html')


@app.route('/Stations/')
def stat():
    stations_dict = {station.id: station.as_dict() for station in stations()}

    return stations_dict


@app.route('/Stations/<station>')
def specific_station(station):
    stations_dict = {station.id: station.as_dict() for station in stations()}
    return jsonify(stations_dict[int(station)])


@app.route('/templates/')
def templ():
    templates_dict = {template.filename: template.to_dict() for template in
                      templates()}
    return templates_dict


@app.route('/templates/<template>')
def specific_template(template):
    metatemplates = template()
    try:
        path = metatemplates[template]['path']

        with open(path, 'r') as f:
            response = make_response(f.read())
            response.headers['Content-type'] = 'text/plain'
            return response
    except KeyError:
        raise InvalidUsage(
            f'{template} template does not exist', status_code=410)


@app.route('/data/')
@nocache
def get_data():
    station_id = request.args.get('station')
    template_name = request.args.get('template')

    valid, template, station, chunk = calculate_data_and_render_from_template(
        template_name=template_name, station_id=station_id)
    # Template_id: Yucheng. The actual file is edam/Yucheng.tmpl
    if valid:
        response = make_response(
            render_template(
                "edam/" +
                template_name +
                '.tmpl',
                chunk=chunk,
                station=station))
        response.headers['Content-type'] = 'text/plain'
        response.headers['Cache-Control'] = 'public, max-age=0'

        # response.headers['Content-Disposition'] = "attachment;
        # filename=test.csv"
        return response
    else:
        if station:
            raise InvalidUsage(
                f'{template_name} template and {station.name} station '
                f'are not compatible',
                status_code=410)
        else:
            raise InvalidUsage('No station', status_code=410)


@app.route('/about/')
def about():
    return render_template('about.html')


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
