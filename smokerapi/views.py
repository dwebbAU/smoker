from smokerapi.models import SensorData, Recipe, Cook, Profile
from smokerapi.serializers import SensorDataSerializer, UserSerializer, RecipeSerializer, CookSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from smokerapi.permissions import OwnsDevice
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
import datetime
from rest_framework.authtoken.models import Token

class SensorDataList(generics.ListCreateAPIView):
  authentication_classes = (TokenAuthentication,SessionAuthentication)
  queryset = SensorData.objects.all()
  serializer_class = SensorDataSerializer
  permission_classes = (permissions.IsAuthenticated,)  

  def perform_create(self, serializer):
      sensordata = serializer.save(controller = self.request.user)
      PIDCont = sensordata.cook.PIDController
      PIDCont.current_error = sensordata.cook.recipe.maxAmbientTemp - sensordata.tempAmbient
      PIDCont.save()
      sensordata.target_speed_fan = PIDCont.target_speed_fan
      sensordata.save()

  def get_queryset(self):
      try:
        since = self.request.META['HTTP_SINCE']
        cook = self.request.META['HTTP_COOK']
        python_time = datetime.datetime.fromtimestamp(int(since)/1000)
        return SensorData.objects.filter(controller__profile__owner=self.request.user,cook__pk=cook,created__gte=python_time)
      except:
        try:
          cook = self.request.META['HTTP_COOK']
          latest = self.request.META['HTTP_LATEST']
          return SensorData.objects.filter(controller__profile__owner = self.request.user,cook__pk=cook).reverse()[:1]
        except:
          try:
            cook = self.request.META['HTTP_COOK']
            return SensorData.objects.filter(controller__profile__owner = self.request.user,cook__pk=cook)
          except:
            return SensorData.objects.filter(controller__profile__owner = self.request.user)



class SensorDataDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = SensorData.objects.all()
  serializer_class = SensorDataSerializer
  permission_classes = (permissions.IsAuthenticated,)

class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
      recipe = serializer.save(owner = self.request.user)


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CookList(generics.ListCreateAPIView):
    queryset = Cook.objects.all()
    serializer_class = CookSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
      try:
        count = self.request.META['HTTP_LATEST']
        return Cook.objects.filter(owner=self.request.user).order_by('-created')[:count]
      except:
        return Cook.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
      
      cook = serializer.save(owner = self.request.user)

class CookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cook.objects.all()
    serializer_class = CookSerializer
    permission_classes = (permissions.IsAuthenticated,)

class UserList(generics.ListCreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticated,)

  def perform_create(self, serializer):
    account = serializer.save()
    profile = Profile.objects.createe(account=account,accountType='CONTROLLER',owner=self.request.user)

class UserDetail(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticated,)

class ControllerList(generics.ListCreateAPIView):
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticated,)

  def perform_create(self, serializer):
    account = serializer.save()
    profile = Profile.objects.create(account=account,accountType='CONTROLLER',owner=self.request.user)
    token = Token.objects.create(user=account)

  def get_queryset(self):
    try:
      controllers = User.objects.filter(profile__accountType='CONTROLLER',profile__owner=self.request.user)
      return controllers
    except User.DoesNotExist:
      raise Http404
      
