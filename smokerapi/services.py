from smokerapi.models import SensorData, Instruction, Recipe, Cook

def calculate_instruction(sensordata):


  if sensordata.cook:
    if sensordata.cook.recipe.max_temp > sensordata.tempAmbient:
      instruction = Instruction.objects.create(speedFan=sensordata.speedFan + 10,cook = sensordata.cook,controller = sensordata.controller)
      instruction.save()


