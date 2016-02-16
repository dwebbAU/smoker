from rest_framework import serializers
from smokerapi.models import SensorData, Instruction, Recipe, Cook
from django.contrib.auth.models import User

class SensorDataSerializer(serializers.ModelSerializer):

  controller = serializers.ReadOnlyField(source='controller.username')

  class Meta:
    model = SensorData
    fields = ('id','tempAmbient','tempInternal','speedFan','controller','cook','target_speed_fan')

class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id','title','max_temp')

class CookSerializer(serializers.ModelSerializer):

  user = serializers.ReadOnlyField(source='owner.username')

  class Meta:
    model = Cook
    fields = ('id','created','complete','controller','recipe','user')

class InstructionSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Instruction
    fields = ('id','speedFan','controller')

class UserSerializer(serializers.ModelSerializer):
  sensordata = serializers.PrimaryKeyRelatedField(many=True,queryset=SensorData.objects.all())

  class Meta:
    model = User
    fields = ('id','username','sensordata')
