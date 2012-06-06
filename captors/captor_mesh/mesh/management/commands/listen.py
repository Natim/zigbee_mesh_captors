# -*- coding: utf-8 -*-
import serial

from django.core.management.base import BaseCommand, CommandError
from captor_mesh.mesh.models import Captor

class Command(BaseCommand):
    args = '<serial portstr>'
    help = 'Listen to a serial port and read information'

    def handle(self, *args, **options):
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
                        infos['arduino_id'] = ord(ser.read())
                        infos['pin_id'] = ord(ser.read())
                        infos['value'] = ord(ser.read())
                        info = Captor.objects.create(**infos)                    
                        print info
                    else:
                        print 'Dropped value :', value
        except KeyboardInterrupt:
            ser.close()
            exit(0)
