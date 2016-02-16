from smokerapi.models import SensorData, Recipe, Cook
from smokerapi.serializers import SensorDataSerializer, UserSerializer, RecipeSerializer, CookSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SensorDataList(generics.ListCreateAPIView):
  queryset = SensorData.objects.all()
  serializer_class = SensorDataSerializer
  permission_classes = (permissions.IsAuthenticated,)  

  def perform_create(self, serializer):
      sensordata = serializer.save(controller = self.request.user)

class SensorDataDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = SensorData.objects.all()
  serializer_class = SensorDataSerializer
  permission_classes = (permissions.IsAuthenticated,)

class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticated,)

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


