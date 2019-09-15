import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request
#from flask_apscheduler import APScheduler
from helpers import figs, flickr

app = Flask(__name__)

#flickr.get_gals()

sched = BackgroundScheduler(daemon=True)
sched.add_job(flickr.get_gals, 'interval', minutes=30)
sched.start()


@app.route('/')
def index():
    feature = 'bar'
    bar = figs.create_plot(feature)
    return render_template('index.html', plot=bar)


@app.route('/awc')
def awc():
    prop_awc = 'flight_category'
    map_awc = figs.create_map_awc(prop_awc)
    return render_template('awc.html', plot=map_awc)


@app.route('/wx')
def wx():
    return render_template('wx.html')


@app.route('/iot')
def iot():
    sensor_iot = 'sensor.load_1m'
    time_iot = 't_100'
    graph_iot = figs.create_graph_iot(sensor_iot, time_iot)
    return render_template('iot.html', plot=graph_iot)


@app.route('/aprs')
def aprs():
    type_aprs = 'prefix'
    prop_aprs = 'altitude'
    time_aprs = 't_100'
    map_aprs = figs.create_map_aprs(type_aprs, prop_aprs, time_aprs)
    return render_template('aprs.html', plot=map_aprs)


@app.route('/aircraft')
def aircraft():
    return render_template('aircraft.html')


@app.route('/paragliding')
def paragliding():
    return render_template('paragliding.html')


@app.route('/soaring')
def soaring():
    return render_template('soaring.html')


@app.route('/n5777v')
def n5777v():
    return render_template('n5777v.html')


@app.route('/galleries')
def galleries():
    rows = flickr.get_gal_rows(6)
    return render_template('galleries.html', rows=rows, title='Galleries')


@app.route('/galleries/<id>')
def gallery(id):
    rows, gals = flickr.get_photo_rows(id, 6)
    return render_template('galleries.html', rows=rows, title=gals[id]['title'])


@app.route('/galleries/<id>/<ph>')
def image(id, ph):
    gals = flickr.load_gals()
    image = {
        'thumb': gals[id]['photos'][ph]['thumb'],
        'large': gals[id]['photos'][ph]['large'],
    }
    return render_template('image.html', image=image, title='photo')


@app.route('/travel')
def travel():
    return render_template('travel.html')


@app.route('/scuba')
def scuba():
    return render_template('scuba.html')


@app.route('/fishing')
def fishing():
    return render_template('fishing.html')


@app.route('/oilgas')
def oilgas():
    return render_template('oilgas.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    graphJSON = figs.create_plot(feature)
    return graphJSON


@app.route('/map_awc', methods=['GET', 'POST'])
def map_awc_change():
    prop_awc = request.args['prop_awc']
    graphJSON = figs.create_map_awc(prop_awc)
    return graphJSON

@app.route('/map_aprs', methods=['GET', 'POST'])
def map_aprs_change():
    type_aprs = request.args['type_aprs']
    prop_aprs = request.args['prop_aprs']
    time_aprs = request.args['time_aprs']
    graphJSON = figs.create_map_aprs(type_aprs, prop_aprs, time_aprs)
    return graphJSON


@app.route('/graph_iot', methods=['GET', 'POST'])
def graph_iot_change():
    sensor_iot = request.args['sensor_iot']
    time_iot = request.args['time_iot']
    graphJSON = figs.create_graph_iot(sensor_iot, time_iot)
    return graphJSON


if __name__ == '__main__':
    app.run(debug=True)
