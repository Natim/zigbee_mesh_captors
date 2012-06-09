# -*- coding: utf-8 -*-
from pymongo import Connection
import random
from time import sleep, time
import datetime

db = Connection().mesh

arduinos = [0xCB]
pins = [14, 15, 16, 17, 18]

starttime = time()

try:
    while True:
        millis = random.randint(500, 2000)
        sleep(millis/1000)

        infos = {}
        infos['arduino'] = arduinos[random.randint(0,len(arduinos)-1)]
        infos['pin'] = pins[random.randint(0,len(pins)-1)]
        infos['value'] = random.randint(0,255)
        infos['date'] = datetime.datetime.utcnow()
        info = db.mesh_captors.save(infos)
        print info, infos

        if (time() - starttime) > 3*60:
            print "\n\nCLEAR OLD DATA\n\n"        
            db.mesh_captors.remove({'date': {'$lt': datetime.datetime.utcnow() - datetime.timedelta(seconds=360)}})
            starttime = time()
    
except KeyboardInterrupt:
    exit(0)
