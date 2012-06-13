# -*- coding: utf-8 -*-
from flask import *
from pymongo import Connection, ASCENDING, DESCENDING
from collections import defaultdict
from bson.code import Code
import datetime

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

    # Result : 

    # [
    #   {label: "Pin 14", data: [[time, point], ...] },
    #   {label: "Pin 15", data: [[time, point], ...] }
    # ]

    values = []

    now = datetime.datetime.utcnow() - datetime.timedelta(seconds=60)
    last_date = False

    for captor in captors_value:
        pin_name = 'Pin %d' % int(captor['pin'])
        date = float(captor['date'].strftime('%H%M%S.%f')[:10])
        if not last_date:
            last_date = date
            last_date -= 100
        dot = [date, int(captor['value'])]
        inside = False
        for pin in values:
            if pin['label'] == pin_name:
                inside = True
                if date > last_date:
                    pin['data'].append(dot)
                break
        if not inside:
            values.append({'label': pin_name, 'data': [dot]})

    response = make_response(json.dumps(values))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
