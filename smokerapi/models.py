from __future__ import unicode_literals

from django.db import models



class Recipe(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.TextField(blank=False)
    max_temp = models.FloatField(blank=False)

    def __unicode__(self):
        return self.title

class Cook(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    controller = models.ForeignKey('auth.User',related_name='cook')
    recipe = models.ForeignKey(Recipe,related_name='cook')
    owner = models.ForeignKey('auth.User',related_name='cooks')

class SensorData(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  tempAmbient = models.FloatField(blank=False)
  tempInternal = models.FloatField(blank=False)
  speedFan = models.IntegerField(blank=False)
  controller = models.ForeignKey('auth.User', related_name='sensordata')
  cook = models.ForeignKey(Cook, related_name='sensordata')

  class Meta:
    ordering = ('created',)

class Instruction(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  speedFan = models.IntegerField(blank=False)
  cook = models.ForeignKey(Cook, related_name='instruction')
  controller = models.ForeignKey('auth.User', related_name='instruction')

  class Meta:
    ordering = ('created',)

class Profile(models.Model):
  ACCOUNT_TYPES = (
    ('USER','User'),
    ('CONTROLLER','Controller'),
  )

  account = models.OneToOneField('auth.User', related_name='profile')
  accountType = models.CharField(max_length=100,choices=ACCOUNT_TYPES)
  owner = models.ForeignKey('auth.User', related_name='controllerprofile', blank=True, null=True)

  def __str__(self):
    return self.account.username
