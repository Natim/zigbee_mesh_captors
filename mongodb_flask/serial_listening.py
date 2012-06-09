# -*- coding: utf-8 -*-
import serial
import datetime
from pymongo import Connection

db = Connection().mesh

ser = serial.Serial(args[0])
ser.open()
if ser.isOpen():
    print 'Listening on :', ser.portstr
else:
    sys.stderr.write('Failed to open serial on : %s\n' % ser.portstr)
    exit(1)

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
                print info
            else:
                print 'Dropped value :', value
except KeyboardInterrupt:
    ser.close()
    exit(0)
