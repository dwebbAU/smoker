from __future__ import unicode_literals

from django.db import models

class SensorData(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  tempAmbient = models.FloatField(blank=False)
  tempInternal = models.FloatField(blank=False)
  speedFan = models.IntegerField(blank=False)
  owner = models.ForeignKey('auth.User', related_name='sensordata')

  class Meta:
    ordering = ('created',)

class Instruction(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  speedFan = models.IntegerField(blank=False)
  sensordata = models.ForeignKey(SensorData,related_name='instructions')

  class Meta:
    ordering = ('created',)
