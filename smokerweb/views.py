from django.shortcuts import render
from smokerapi.models import SensorData,Cook,Recipe

def Index(request):
    return render(request,'smokerweb/index.html')
