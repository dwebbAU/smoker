from django.contrib import admin
from smokerapi.models import SensorData, Recipe, Cook, Profile

# Register your models here.

admin.site.register(SensorData)
admin.site.register(Recipe)
admin.site.register(Cook)
admin.site.register(Profile)

