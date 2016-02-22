from django.shortcuts import render
from smokerapi.models import SensorData, Cook, Recipe
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def Landing(request):
  try:
    cooks = Cook.objects.filter(owner=request.user)
    try: 
      current_cook = cooks.filter(complete=False).latest('created')
      return redirect('cook_dashboard',pk=current_cook.pk)
    except Cook.DoesNotExist:
      return render(request,'smokerweb/nocook.html')
  except Cook.DoesNotExist:
    return render(request, 'smokerweb/nocook.html')  


def CookDashboard(request,pk):

    cook = Cook.objects.get(pk=pk)
    cooks = Cook.objects.filter(owner=request.user)
    controllers = User.objects.filter(profile__owner=request.user)
    recipes = Recipe.objects.filter(owner=request.user)

    context = {'cook':cook,'cooks':cooks,'controllers':controllers,'recipes':recipes}

    return render(request,'smokerweb/cookdashboard.html',context)
