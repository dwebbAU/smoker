from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class Recipe(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.TextField(blank=False)
    max_temp = models.FloatField(blank=False)

    def __unicode__(self):
        return self.title

class Cook(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    controller = models.ForeignKey('auth.User',related_name='cook',limit_choices_to={'profile__accountType':'CONTROLLER'})
    recipe = models.ForeignKey(Recipe,related_name='cook')
    owner = models.ForeignKey('auth.User',related_name='cooks',limit_choices_to={'profile__accountType':'USER'})

    def clean(self):
        for cook in self.controller.cook.all():
          if not cook.complete and cook != self:
            raise ValidationError(_('Controller is already involved in an active cook.'))

    def __str__(self):
      return self.created.strftime('%d/%m/%y') + " - " + self.recipe.title + " (" + self.owner.username + ")"

class SensorData(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  tempAmbient = models.FloatField(blank=False)
  tempInternal = models.FloatField(blank=False)
  speedFan = models.IntegerField(blank=False)
  controller = models.ForeignKey('auth.User', related_name='sensordata',limit_choices_to={'profile__accountType':'CONTROLLER'})
  cook = models.ForeignKey(Cook, related_name='sensordata',blank=True,null=True)

  class Meta:
    ordering = ('created',)
    verbose_name = 'Reading'

  def __str__(self): 
    return self.created.strftime('%H:%M:%S') + " - " + self.controller.username

  def save(self, *args, **kwargs):
    try:
     for cook in self.controller.cook.filter(complete=False): 
        self.cook = cook
        super(SensorData,self).save(*args, **kwargs)
    except Cook.DoesNotExist:
      return

  def calculate_target_speed_fan(self):
    if self.cook:
      if self.cook.recipe.max_temp > self.tempAmbient:
        target_speed_fan = self.speedFan + 10
        return target_speed_fan
      elif self.cook.recipe.max_temp < self.tempAmbient:
        target_speed_fan = self.speedFan - 10
        return target_speed_fan
    else:
      return 0
  
  target_speed_fan = property(calculate_target_speed_fan)  


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
