# Create your views here.

from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

import json
from collections import defaultdict

from captor_mesh.mesh.models import Captor
from captor_mesh.mesh.forms import ArduinoForm

import operator

def index(request):

    if request.method == "POST":
        form = ArduinoForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse(form.cleaned_data['view'], args=[form.cleaned_data['arduino']]))

    form = ArduinoForm()
    return render_to_response('mesh/index.html', {'form': form}, 
                              RequestContext(request))

def gauge_api(request, arduino_id):
    captors_value = Captor.objects.filter(arduino_id=arduino_id).order_by('-date_time')

    captors = {}

    for captor in captors_value:
        if not captor.pin_id in captors:
            captors[captor.pin_id] = captor

    captors_values = [['Pin %s' % x.pin_id, x.value] for x in captors.values()]
    

    return HttpResponse(json.dumps(captors_values), mimetype="application/json")

def gauge(request, arduino_id):
    return render_to_response('mesh/gauge.html', {'arduino': arduino_id})
    

def line_api(request, arduino_id):
    captors_value = Captor.objects.filter(arduino_id=arduino_id).order_by('pin_id', '-date_time')

    captors = {}
    values = defaultdict(int);
    pins = []
    
    for captor in captors_value:
        pin_name = 'Pin %d' % captor.pin_id
        if  pin_name not in pins:
            pins.append(pin_name)
        values[pin_name] = captor.value
        captors[captor.date_time.strftime('%M%S')] = defaultdict(int, values)

    captors_values = []
    sorted_captors = sorted(captors.iteritems(), key=lambda x: x[0])

    captors_values.append(['x']+pins)
    for time, values_dict in sorted_captors:
        result = [time]
        for pin in pins:            
            result.append(values_dict[pin])
        captors_values.append(result)

    return HttpResponse(json.dumps(captors_values), mimetype="application/json") 

def line(request, arduino_id):
    return render_to_response('mesh/line.html', 
                              {'arduino': arduino_id})

def flot(request, arduino_id):
    return render_to_response('mesh/flot.html', 
                              {'arduino': arduino_id})

def flot_api(request, arduino_id):
    captors_value = Captor.objects.filter(arduino_id=arduino_id).order_by('pin_id', '-date_time')
    
    captors = {}
    values = defaultdict(int);
    pins = []
    
    for captor in captors_value:
        pin_name = 'Pin %d' % captor.pin_id
        if  pin_name not in pins:
            pins.append(pin_name)
        values[pin_name] = captor.value
        captors[captor.date_time.strftime('%M%S')] = defaultdict(int, values)

    sorted_captors = sorted(captors.iteritems(), key=lambda x: x[0])

    print sorted_captors
