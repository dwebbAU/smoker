from django.shortcuts import render
from smokerapi.models import SensorData, Cook, Recipe
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

@login_required
def CookDashboard(request):

    cooks = Cook.objects.filter(owner=request.user)
    controllers = User.objects.filter(profile__owner=request.user)
    recipes = Recipe.objects.filter(owner=request.user)

    context = {'cooks':cooks,'controllers':controllers,'recipes':recipes}

    return render(request,'smokerweb/cookdashboard.html',context)
