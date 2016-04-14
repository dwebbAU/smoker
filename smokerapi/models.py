from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import utc
from clickatell.rest import Rest

class Recipe(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(blank=False, max_length=100)
    targetInternalTemp = models.FloatField(blank=False)
    maxAmbientTemp = models.FloatField(blank=False)
    owner = models.ForeignKey('auth.User',related_name='recipes',limit_choices_to={'profile__accountType':'USER'},null=False,blank=False)

    def __str__(self):
        return self.title


class Cook(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    controller = models.ForeignKey('auth.User',related_name='cook',limit_choices_to={'profile__accountType':'CONTROLLER'})
    recipe = models.ForeignKey(Recipe,related_name='cook')
    owner = models.ForeignKey('auth.User',related_name='cooks',limit_choices_to={'profile__accountType':'USER'})
    warning = models.BooleanField(default=False)
    warning_type = models.CharField(max_length=100,blank=True,null=True)
    warning_message = models.CharField(max_length=200,blank=True,null=True)
    pending_mop = models.BooleanField(default=False)

#    def clean(self):
#        for cook in self.controller.cook.all():
#          if not cook.complete and cook != self:
#            raise ValidationError(_('Controller is already involved in an active cook.'))

    def __str__(self):
      return self.created.strftime('%d/%m/%y') + " - " + self.recipe.title


    def save(self,*args,**kwargs):
      if self.complete:
        all_readings = self.sensordata.all()
        last_reading = all_readings[0]
        for reading in all_readings:
          if ((reading.pk != last_reading.pk) and (abs((reading.tempAmbient - last_reading.tempAmbient)) < 2 )):  
            reading.delete()
          else:
            last_reading = reading
      for cook in self.controller.cook.all():
        if not cook.complete and cook != self:
          raise ValidationError(_('Controller is already involved in an active cook.'))
      super(Cook,self).save(*args,**kwargs) 



class PIDController(models.Model):
  Kp = models.PositiveSmallIntegerField(default=1,blank=False,null=False)
  Kd = models.PositiveSmallIntegerField(default=1,blank=False,null=False)
  Ki = models.PositiveSmallIntegerField(default=1,blank=False,null=False)
  Cp = models.IntegerField(default=0,blank=False,null=False)
  Ci = models.IntegerField(default=0,blank=False,null=False)
  Cd = models.IntegerField(default=0,blank=False,null=False)
  current_error = models.IntegerField(default=0,blank=False,null=False)
  previous_error = models.IntegerField(default=0,blank=False,null=False)
  current_time = models.DateTimeField(default=datetime.now,blank=True,null=True)
  previous_time = models.DateTimeField(default=datetime.now,blank=True,null=True)
  cook = models.OneToOneField(Cook,related_name='PIDController')

  def calculate_target_speed_fan(self):

    
    self.current_time = timezone.now()

    timediff = self.current_time - self.previous_time
    dt = timediff.total_seconds()
    de = self.current_error - self.previous_error

    self.Cp = self.Kp * self.current_error


    if int(dt) > 0:
      self.Ci += self.current_error/int(dt)
    
  
    self.Cd = 0
    if int(dt) > 0:
      self.Cd = de/int(dt)

    self.previous_time = self.current_time
    self.previous_error = self.current_error


    self.save()
    result = self.Cp + (self.Ki * self.Ci) - (self.Kd * self.Cd)
    if result > 100:
      result = 100
    if result < 10:
      result = 10
    
    return result 

  target_speed_fan = property(calculate_target_speed_fan)


class SensorData(models.Model):
  created = models.DateTimeField(auto_now_add=True)
  tempAmbient = models.FloatField(blank=False)
  tempInternal = models.FloatField(blank=False)
  speedFan = models.IntegerField(blank=False)
  heap = models.FloatField(blank=False)
  controller = models.ForeignKey('auth.User', related_name='sensordata',limit_choices_to={'profile__accountType':'CONTROLLER'})
  cook = models.ForeignKey(Cook, related_name='sensordata',blank=True,null=True)
  target_speed_fan = models.IntegerField(blank=True,null=True)
 
  def determine_mop(self):
    if self.cook.pending_mop:
      self.cook.pending_mop = False
      self.cook.save()
      return True
    else:
      return False

  mop = property(determine_mop)


  class Meta:
    ordering = ('created',)
    verbose_name = 'Reading'

  def __str__(self): 
    return self.created.strftime('%H:%M:%S') + " - " + self.controller.username

  def save(self, *args, **kwargs):
    try:
     for cook in self.controller.cook.filter(complete=False): 
        self.cook = cook
        if(cook.warning and cook.warning_type == 'TIMEOUT'):
          cook.warning = False
          cook.save()
        if(cook.recipe.maxAmbientTemp - self.tempAmbient > 20):
          if (not (cook.warning and cook.warning_type == 'TEMP')):
            cook.warning = True
            cook.warning_type = "TEMP"
            cook.warning_message = "Temperature is well below target!"
            cook.save()
            clickatell = Rest('GRf1iv_FtCiU6tpabzKZsCpJlewGgOaeeftpAE72biY7I.4SbGdio20MPoH_Gz')
            clickatell.sendMessage(['+61431744144'], "Smoker in strife! Temperature is well below target mang")


        else:
          if(cook.warning == True and cook.warning_type == "TEMP"):
            cook.warning = False
            cook.save()

        super(SensorData,self).save(*args, **kwargs)
    except Cook.DoesNotExist:
      return

class Profile(models.Model):
  ACCOUNT_TYPES = (
    ('USER','User'),
    ('CONTROLLER','Controller'),
  )

  account = models.OneToOneField('auth.User', related_name='profile')
  accountType = models.CharField(max_length=100,choices=ACCOUNT_TYPES)
  owner = models.ForeignKey('auth.User', related_name='controllerprofile', blank=True, null=True, limit_choices_to={'profile__accountType':'USER'})


  def clean(self):
      if self.accountType == 'CONTROLLER' and self.owner is None:
        raise ValidationError(_('A Controller must have an Owner.'))

  def __str__(self):
    return self.account.username
