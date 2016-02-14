from smokerapi.models import SensorData, Instruction

def calculate_fanSpeed(instruction):
  instruction.speedFan = instruction.sensordata.speedFan / 2 
  instruction.save()
