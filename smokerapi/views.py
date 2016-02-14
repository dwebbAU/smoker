from smokerapi.models import SensorData, Instruction
from smokerapi.serializers import SensorDataSerializer, UserSerializer, InstructionSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from smokerapi.services import calculate_fanSpeed

class SensorDataList(generics.ListCreateAPIView):
  queryset = SensorData.objects.all()
  serializer_class = SensorDataSerializer
  permission_classes = (permissions.IsAuthenticated,)  

  def perform_create(self, serializer):
    sensordata = serializer.save(owner = self.request.user)
    instruction = Instruction.objects.create(sensordata = sensordata,speedFan=30)
    calculate_fanSpeed(instruction)

class SensorDataDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = SensorData.objects.all()
  serializer_class = SensorDataSerializer
  permission_classes = (permissions.IsAuthenticated,)

class InstructionDetail(generics.RetrieveAPIView):
  queryset = Instruction.objects.all()
  serializer_class = InstructionSerializer
  permission_classes = (permissions.IsAuthenticated,)

class UserList(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticated,)

class UserDetail(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticated,)


