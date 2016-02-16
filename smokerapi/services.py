from smokerapi.models import SensorData, Instruction, Recipe, Cook

def calculate_instruction(cook, sensordata):

    if cook.recipe.max_temp > sensordata.tempAmbient:
        instruction = Instruction.objects.create(speedFan=sensordata.speedFan + 10,cook = cook,controller = sensordata.controller)
        instruction.save()


