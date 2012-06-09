# -*- coding: utf-8 -*-
from flask import *
from pymongo import Connection, ASCENDING, DESCENDING
from collections import defaultdict
from bson.code import Code

app = Flask(__name__)
db = Connection().mesh

@app.route('/')
def index():
    mapper = Code("""
                  function () {
                      emit(this.arduino, 1);
                  }
                  """)
    reducer = Code("""
                  function (key, values) {
                      return 1;
                  }
                  """)
    try:
        arduinos = db.mesh_captors.map_reduce(mapper, reducer, "arduinos").find()
        arduinos_id = [(int(x['_id']), str(hex(int(x['_id'])))) for x in arduinos]
        return render_template('index.html', arduinos=arduinos_id)
    except:
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
    captors_value = db.mesh_captors.find({'arduino': int(arduino_id)}, 
                                         sort=[('pin', ASCENDING), 
                                               ('date', DESCENDING)])
    captors = {}

    for captor in captors_value:
        pin = int(captor['pin'])
        if not pin in captors:
            captors[pin] = captor

    captors_values = [['Pin %s' % int(x['pin']), int(x['value'])] for x in captors.values()]

    response = make_response(json.dumps(captors_values))
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
    
    for captor in captors_value:
        pin_name = 'Pin %d' % int(captor['pin'])
        if pin_name not in pins:
            pins.append(pin_name)
        values[pin_name] = int(captor['value'])
        captors[captor['date'].strftime('%M%S')] = defaultdict(int, values)

    captors_values = []
    sorted_captors = sorted(captors.iteritems(), key=lambda x: x[0])

    captors_values.append(['x']+pins)
    for time, values_dict in sorted_captors:
        result = [time]
        for pin in pins:
            result.append(values_dict[pin])
        captors_values.append(result)

    response = make_response(json.dumps(captors_values))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
