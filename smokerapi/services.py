from smokerapi.models import SensorData, Instruction, Recipe, Cook

def calculate_instruction(cook_set, sensordata):

    try:
        cook = cook_set.get(controller=sensordata.controller)
    except Cook.DoesNotExist:
        return

    if cook.recipe.max_temp > sensordata.tempAmbient:
        instruction = Instruction.objects.create(speedFan=sensordata.speedFan + 10,cook = cook,controller = sensordata.controller)
        instruction.save()


