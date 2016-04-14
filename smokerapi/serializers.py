from rest_framework import serializers
from smokerapi.models import SensorData, Recipe, Cook
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class SensorDataSerializer(serializers.ModelSerializer):

  controller = serializers.ReadOnlyField(source='controller.username')

  class Meta:
    model = SensorData
    fields = ('created','id','tempAmbient','tempInternal','speedFan','heap','controller','cook','target_speed_fan','mop')

class RecipeSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Recipe
        fields = ('id','title','targetInternalTemp','maxAmbientTemp','owner')



class CookSerializer(serializers.ModelSerializer):

  user = serializers.ReadOnlyField(source='owner.username')

  class Meta:
    model = Cook
    fields = ('id','created','complete','controller','recipe','user','warning','warning_message')

class UserSerializer(serializers.ModelSerializer):
#  sensordata = serializers.PrimaryKeyRelatedField(many=True,queryset=SensorData.objects.all())

  class Meta:
    model = User
    fields = ('id','username')
