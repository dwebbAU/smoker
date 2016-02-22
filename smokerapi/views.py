from smokerapi.models import SensorData, Recipe, Cook
from smokerapi.serializers import SensorDataSerializer, UserSerializer, RecipeSerializer, CookSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from smokerapi.permissions import OwnsDevice
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
import datetime

class SensorDataList(generics.ListCreateAPIView):
  authentication_classes = (TokenAuthentication,SessionAuthentication)
  queryset = SensorData.objects.all()
  serializer_class = SensorDataSerializer
  permission_classes = (permissions.IsAuthenticated,)  

  def perform_create(self, serializer):
      sensordata = serializer.save(controller = self.request.user)


  def get_queryset(self):
      try:
        since = self.request.META['HTTP_SINCE']
        cook = self.request.META['HTTP_COOK']
        python_time = datetime.datetime.fromtimestamp(int(since)/1000)
        return SensorData.objects.filter(controller__profile__owner=self.request.user,cook__pk=cook,created__gte=python_time)
      except:
        try:
          cook = self.request.META['HTTP_COOK']
          return SensorData.objects.filter(controller__profile__owner = self.request.user,cook__pk=cook)
        except:
          return SensorData.objects.filter(controller__profile__owner = self.requets.user)


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

    def perform_create(self, serializer):
      cook = serializer.save(owner = self.request.user)

class CookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cook.objects.all()
    serializer_class = CookSerializer
    permission_classes = (permissions.IsAuthenticated,)

class UserList(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticated,)

class UserDetail(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticated,)

class ControllerList(generics.ListCreateAPIView):
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticated,)

  def get_queryset(self):
    try:
      controllers = User.objects.filter(profile__accountType='CONTROLLER',profile__owner=self.request.user)
      return controllers
    except User.DoesNotExist:
      raise Http404
      
