# -*- coding: utf-8 -*- 
from django.utils.translation import ugettext_lazy as _
from django.db import models

class Captor(models.Model):
    arduino_id = models.PositiveIntegerField(_('Arduino ID'))
    pin_id = models.PositiveIntegerField(_('PIN ID'))
    value = models.PositiveIntegerField(_('Captor value'))
    date_time = models.DateTimeField(_('Heure de saisie'), auto_now_add=True)

    class Meta:
        ordering = ['date_time']
        verbose_name = _('captor')

    def __unicode__(self):
        return u'[%s] Arduino : %s - PIN : %s - Value : %d' % (self.date_time.strftime('%H:%M:%S'),
                                                               self.arduino_id,
                                                               self.pin_id,
                                                               self.value)
