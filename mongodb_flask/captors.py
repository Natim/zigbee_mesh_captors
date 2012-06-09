# -*- coding: utf-8 -*-
from flask import *
from pymongo import Connection, ASCENDING, DESCENDING
from collections import defaultdict
from bson.code import Code
from time import time

app = Flask(__name__)
db = Connection().mesh

db.mesh_captors.ensure_index([('arduino', ASCENDING), ('pin', ASCENDING), ('date', DESCENDING)])

@app.route('/')
def index():
    arduinos = db.mesh_captors.distinct('arduino')
    arduinos_id = [(x, str(hex(x))) for x in arduinos]
    if len(arduinos_id) > 0:
        return render_template('index.html', arduinos=arduinos_id)
    else:
        return render_template('nodata.html', database=db.name)

@app.route('/', methods=['POST'])
def routing():
    return redirect('%s/%s/' % (request.form['view'],
                                request.form['arduino']))

@app.route('/gauge/<arduino_id>/')
def gauge(arduino_id):
    return render_template('gauge.html', arduino=arduino_id)

@app.route('/gauge_api/<arduino_id>/')
def gauge_api(arduino_id):
    # We keep only the last value ordered by date
    reducer = Code("""
                  function (doc, out) {
                      if(out.date == 0 || out.date < doc.date) {
                           out.date = doc.date;
                           out.value = doc.value;
                      }
                  }
                  """)

    # We group lines by pin of the arduino
    captors_values = db.mesh_captors.group(
        key=['pin'], 
        condition={'arduino': int(arduino_id)}, 
        reduce=reducer, initial={'date': 0})
    
    response = make_response(json.dumps([
                [u'Pin %s' % x['pin'], int(x['value'])] \
                    for x in captors_values]))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/line/<arduino_id>/')
def line(arduino_id):
    return render_template('line.html', arduino=arduino_id)

@app.route('/line_api/<arduino_id>/')
def line_api(arduino_id):
    captors_value = db.mesh_captors.find({'arduino': int(arduino_id)},
                                         sort=[('pin', ASCENDING), 
                                               ('date', DESCENDING)])

    captors = {}
    values = defaultdict(int);
    pins = []

    last_pin_value = defaultdict(int)

    for captor in captors_value:
        pin_name = 'Pin %d' % int(captor['pin'])
        if pin_name not in pins:
            pins.append(pin_name)
        values[pin_name] = int(captor['value'])
        captors[captor['date'].strftime('%H%M%S.%f')[1:8]] = dict(values)

    captors_values = []
    sorted_captors = sorted(captors.iteritems(), key=lambda x: x[0])

    captors_values.append(['x']+pins)
    for time, values_dict in sorted_captors:
        result = [time]
        for pin in pins:
            try:
                result.append(values_dict[pin])
                last_pin_value[pin] = values_dict[pin]
            except KeyError:
                result.append(last_pin_value[pin])
        captors_values.append(result)
    
    captors = [captors_values[0]] + captors_values[1:][-50:]
    response = make_response(json.dumps(captors))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
