# -*- coding: utf-8 -*-
from django import forms
from models import Captor

def get_arduinos():
    arduinos = set(Captor.objects.values_list('arduino_id', flat=True))
    return [(x, u'Arduino 0x%x' % x) for x in sorted(arduinos)]

class ArduinoForm(forms.Form):
    arduino = forms.ChoiceField(label="Arduino ID")
    view = forms.ChoiceField(label="Vue", choices=(('gauge', 'Gauge'),
                                                   ('line', 'Line')))

    def __init__(self, *args, **kwargs):
        super(ArduinoForm, self).__init__(*args, **kwargs)
        self.fields['arduino'].choices = get_arduinos()

