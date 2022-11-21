from math import pow    
from LifeFitness.models import Exercise

# Given the weight and height of User it will return 
# the according BMI of that User
def convertBMI(weight, height):
    weightInkgs = weight * 0.45359237
    heightIncm = height * 0.3048
    return (weightInkgs / pow(heightIncm, 2))

# Returns the current list of available Exercises 
# Exercise List will be in the following List format: 
# ExList = (
#   (1, exercise.name), 
#   (2, exercise.name), 
#   (3, exercise.name), 
#   ... 
# )
def ExerciseList(): 
    ExList = []
    for exercise in Exercise.objects.all():
        ExList.append((exercise.pk, exercise.name))
    return (tuple(ExList))