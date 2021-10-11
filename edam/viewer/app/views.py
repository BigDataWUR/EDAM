from flask import render_template
from flask import request, make_response, jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

from edam.viewer.app import app, calculate_metastations, nocache, calculate_templates, \
    calculate_data_and_render_from_template
from edam.viewer.app.InvalidUsage import InvalidUsage
from edam.viewer.app.OGC_SOS import OGC_SOS

GoogleMaps(app)


@app.route('/maps/')
@app.route('/index/')
@app.route('/')
def mapview():
    # creating a map in the view
    metastations = calculate_metastations()
    markers = list()
    for station_id in metastations:
        station_dict = metastations[station_id]
        if station_dict['latitude'] is not None and station_dict['longitude'] is not None:
            observables = ', '.join(
                [station_dict['observables'][temp_id]['observable'] for temp_id in station_dict['observables']])
            
            infobox = '<p><b>Station</b>: <a href="%sStations/%s" target="_blank">%s</a></p>' \
                      '<p><b>Quantities</b>: %s</p>' % (
                          request.url_root, station_id, station_dict['name'], observables)
            temp_dict = {'lat': station_dict['latitude'], 'lng': station_dict['longitude'], 'infobox': infobox}
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
    return render_template('error.html', errorTitle=str(error.status_code), errorMessage=error.message)


@app.route('/home/')
def index():
    return render_template('home.html')


@app.route('/Stations/')
def stations():
    metastations = calculate_metastations()
    return jsonify(metastations)


@app.route('/Stations/<station>')
def specific_station(station):
    metastations = calculate_metastations()
    return jsonify(metastations[int(station)])


@app.route('/templates/')
def templates():
    metatemplates = calculate_templates()
    return jsonify(metatemplates)


@app.route('/templates/<template>')
def specific_template(template):
    metatemplates = calculate_templates()
    try:
        path = metatemplates[template]['path']
        
        with open(path, 'r') as f:
            response = make_response(f.read())
            response.headers['Content-type'] = 'text/plain'
            return response
    except KeyError:
        raise InvalidUsage(f'{template} template does not exist', status_code=410)


@app.route('/data/')
@nocache
def get_data():
    station_id = request.args.get('station')
    observable_id = request.args.get('template')
    
    valid, template, station, chunk = calculate_data_and_render_from_template(observable_id=observable_id,
                                                                              station_id=station_id)
    # Template_id: Yucheng. The actual file is edam/Yucheng.tmpl
    if valid:
        response = make_response(render_template("edam/" + observable_id + '.tmpl', chunk=chunk, station=station))
        response.headers['Content-type'] = 'text/plain'
        response.headers['Cache-Control'] = 'public, max-age=0'
        
        # response.headers['Content-Disposition'] = "attachment; filename=test.csv"
        return response
    else:
        if station:
            raise InvalidUsage('%s template and %s station are not compatible' % (observable_id, station.name),
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
    
    sos = OGC_SOS(sos_request, sos_procedure, sos_offering, sos_event_time, sos_observed_property)
    sos_response = sos
    
    response = make_response(render_template(sos_response.template
                                             , info=sos.info
                                             , keywords=sos.keywords
                                             , stations=sos.stations
                                             , helpers=sos.metadata
                                             , procedure=sos.procedure
                                             , sensor=sos.sensor
                                             , results=sos.results
                                             , helper=sos.helper_object))
    response.headers["Content-Type"] = "application/xml"
    
    return response


if __name__ == "__main__":
    pass
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    # app.run(debug=True)
