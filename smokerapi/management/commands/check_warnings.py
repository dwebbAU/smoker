from django.core.management.base import BaseCommand, CommandError
from smokerapi.models import Cook, SensorData
from datetime import datetime
from django.utils import timezone
from clickatell.rest import Rest


def send_sms(message):
  clickatell = Rest('GRf1iv_FtCiU6tpabzKZsCpJlewGgOaeeftpAE72biY7I.4SbGdio20MPoH_Gz')
  response = clickatell.sendMessage(['+61431744144'],message)
  print(response)


class Command(BaseCommand):
  
  def handle(self, *args, **options):
    for cook in Cook.objects.filter(complete=False):
      if(cook.created.minute == datetime.now().minute):
        cook.pending_mop = True
        cook.save()

      latest_reading = SensorData.objects.filter(cook=cook).latest('created')

      if ((timezone.now() - latest_reading.created).seconds > 300):
        if( not (cook.warning and cook.warning_type == 'TIMEOUT')):
          cook.warning = True
          cook.warning_type = 'TIMEOUT'
          cook.warning_message = "Controller has not communicated in at least 5 minutes"
          cook.save()
          send_sms("Smoker in strife!! Controller has not communicated in at least 5 minutes")

       
