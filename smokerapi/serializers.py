from rest_framework import serializers
from smokerapi.models import SensorData, Instruction
from django.contrib.auth.models import User

class SensorDataSerializer(serializers.ModelSerializer):

  owner = serializers.ReadOnlyField(source='owner.username')
  instructions = serializers.PrimaryKeyRelatedField(many=True,read_only=True)

  class Meta:
    model = SensorData
    fields = ('id','tempAmbient','tempInternal','speedFan','owner','instructions')

class InstructionSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Instruction
    fields = ('id','speedFan')

class UserSerializer(serializers.ModelSerializer):
  sensordata = serializers.PrimaryKeyRelatedField(many=True,queryset=SensorData.objects.all())

  class Meta:
    model = User
    fields = ('id','username','sensordata')
