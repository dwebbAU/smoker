import RPi.GPIO as GPIO
import time
import urllib2
from random import randint
import simplejson
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

SENSOR_URL = "http://192.168.32.120/sensordata/"
INSTRUCTION_URL = "http://192.168.32.120/instructions/"
API_PORT = "80"
HEADERS = {'Content-type':'application/json','Accept':'application/json'}
API_USERNAME = 'pi'
API_PASSWORD = 'letmein'

while True:
  data = {'tempAmbient':randint(0,100),'tempInternal':randint(0,100),'speedFan':randint(0,100)}
  r = requests.post(SENSOR_URL,data=simplejson.dumps(data),headers=HEADERS,auth=(API_USERNAME,API_PASSWORD))
  instruction = requests.get(INSTRUCTION_URL,auth=(API_USERNAME,API_PASSWORD))
  print(instruction.text)
  time.sleep(15)

