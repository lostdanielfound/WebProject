from math import pow
import pandas as pd 
from LifeFitness.models import Exercise

# Given the weight and height of User it will return 
# the according BMI of that User
def convertBMI(weight, height):
    weightInkgs = weight * 0.45359237
    heightIncm = height * 0.3048
    return (weightInkgs / pow(heightIncm, 2))

# Returns the current list of User made Exercises 
# Exercise List will be in the following List format: 
# ExList = (
#   (1, exercise.name), 
#   (2, exercise.name), 
#   (3, exercise.name), 
#   ... 
# )
 
def CurrentExerciseList(): 
    ExList = []
    for exercise in Exercise.objects.all():
        ExList.append((exercise.pk, exercise.name))
    return (tuple(ExList))

# Returns the list of static defined exercises from 
# the excel sheet from Exercise_sample.xls within the assets folder
# Using pandas to export the column and return a tuple of exercises
# ExList = (
#   ("exercise name"),
#   ("exercise name"), 
#       ...
# )

def CompleteExerciseList(): 
    data = pd.read_excel("./LifeFitness/static/assets/Exercise_sample.xls")
    df = pd.DataFrame(data, columns=['Exercise'])

    ExList = list()  
    for arr in df.values.tolist():
        ExList.append(arr[0])
    return(tuple(ExList))

