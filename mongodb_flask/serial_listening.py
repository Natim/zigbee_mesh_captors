# -*- coding: utf-8 -*-
import sys
import serial
import datetime
from time import time
from pymongo import Connection

db = Connection().mesh

if len(sys.argv) < 2:
    sys.stderr.write('You must provide the serial port to open')
    sys.exit(0)

ser = serial.Serial(sys.argv[1])
starttime = time()

if ser.isOpen():
    print 'Listening on :', ser.portstr
else:
    try:
        ser.open()
        if ser.isOpen():
            print 'Listening on :', ser.portstr
        else:
            sys.stderr.write('Failed to open serial on : %s\n' % ser.portstr)
            exit(1)            
    except:
        pass

try:
    while ser.isOpen():
        if ser.inWaiting() > 3:
            value = ord(ser.read())
            if value == 0x7E:
                infos = {}
                infos['arduino'] = ord(ser.read())
                infos['pin'] = ord(ser.read())
                infos['value'] = ord(ser.read())
                infos['date'] = datetime.datetime.utcnow()
                info = db.mesh_captors.save(infos)
                print infos
            else:
                print 'Dropped value :', value

        if (time() - starttime) > 5*60:
            print "\n\nCLEAR OLD DATA\n\n"        
            db.mesh_captors.remove({'date': {'$lt': datetime.datetime.utcnow() - datetime.timedelta(seconds=5*60)}})
            starttime = time()

except KeyboardInterrupt:
    ser.close()
    exit(0)
