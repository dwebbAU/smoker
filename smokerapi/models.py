from __future__ import unicode_literals

from django.db import models



class SensorData(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  tempAmbient = models.FloatField(blank=False)
  tempInternal = models.FloatField(blank=False)
  speedFan = models.IntegerField(blank=False)
  controller = models.ForeignKey('auth.User', related_name='sensordata')

  class Meta:
    ordering = ('created',)

class Recipe(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.TextField(blank=False)
    max_temp = models.FloatField(blank=False)

    def __unicode__(self):
        return self.title

class Cook(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    controller = models.OneToOneField('auth.User',related_name='cook')
    recipe = models.ForeignKey(Recipe,related_name='cook')
    owner = models.ForeignKey('auth.User',related_name='cooks')

class Instruction(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  speedFan = models.IntegerField(blank=False)
  cook = models.ForeignKey(Cook, related_name='instruction')
  controller = models.ForeignKey('auth.User', related_name='instruction')

  class Meta:
    ordering = ('created',)