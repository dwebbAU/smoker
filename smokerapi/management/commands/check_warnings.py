from django.core.management.base import BaseCommand, CommandError
from smokerapi.models import Cook, SensorData
from datetime import datetime
from django.utils import timezone
from clickatell.rest import Rest
from django.conf import settings

def send_sms(message,cook):
  if(settings.SMS and (timezone.now() - cook.last_notify).seconds > 300):
    clickatell = Rest('GRf1iv_FtCiU6tpabzKZsCpJlewGgOaeeftpAE72biY7I.4SbGdio20MPoH_Gz')
    response = clickatell.sendMessage(['+61431744144'],message)
    cook.last_notify = timezone.now()
    cook.save()
#'+61425330662'],message)


class Command(BaseCommand):
  
  def handle(self, *args, **options):
    for cook in Cook.objects.filter(complete=False):

# Check Pending Mop
      if(cook.created.minute == datetime.now().minute):
        cook.pending_mop = True
        cook.save()


      latest_reading = SensorData.objects.filter(cook=cook).latest('created')

# Check Last Reading
      if ((timezone.now() - latest_reading.created).seconds > 300):
        if( not(cook.warning_type == 'TIMEOUT') ):
          cook.warning = True
          cook.warning_type = 'TIMEOUT'
          cook.warning_message = "Controller has not communicated in at least 5 minutes"
          cook.save()
          send_sms("Smoker in strife!! Controller has not communicated in at least 5 minutes",cook)
      else:
        if (cook.warning_type == 'TIMEOUT'):
          cook.warning = False
          cook.warning_type = ""
          cook.warning_message = ""
          cook.save() 
#          send_sms("Smoker happy again - Controller has communicated",cook)

      if (latest_reading.heap < 10000):
        if (not(cook.warning_type == 'HEAP') ):
          cook.warning = True
          cook.warning_type = 'HEAP'
          cook.warning_message = "Controller is low on memory"
          cook.save()
          send_sms("Smoker in strife!! Controller is low on memory!",cook)
      else:
        if (cook.warning_type == 'HEAP'):
          cook.warning = False
          cook.warning_type = ""
          cook.warning_message = ""
          cook.save()
#          send_sms("Smoker happy again - Controller memory is sufficient",cook)

      if (abs(latest_reading.tempAmbient - latest_reading.cook.recipe.maxAmbientTemp) > 20):
        if (not(cook.warning_type == 'TEMP')):
          cook.warning = True
          cook.warning_type = 'TEMP'
          cook.warning_message = "Ambient temp deviation from target"
          cook.save()
          send_sms("Smoker in strife!! Ambient temp way off target",cook)
      else:
        if (cook.warning_type == 'TEMP'):
          cook.warning = False
          cook.warning_type = ""
          cook.warning_message = ""
          cook.save()
#          send_sms("Smoker happy again - Ambient temp within range",cook)


