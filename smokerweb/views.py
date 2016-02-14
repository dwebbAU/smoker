from django.shortcuts import render
from smokerapi.models import SensorData, Cook, Recipe
from django.contrib.auth.decorators import login_required

@login_required
def Index(request):
    cook = Cook.objects.latest('created')
    context = {'tempAmbient':SensorData.objects.filter(controller=cook.controller).latest('created').tempAmbient,'tempInternal':SensorData.objects.filter(controller=cook.controller).latest('created').tempInternal}
    return render(request,'smokerweb/index.html',context)
