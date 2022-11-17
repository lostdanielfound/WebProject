from math import pow    

# Given the weight and height of User it will return 
# the according BMI of that User
def convertBMI(weight, height):
    weightInkgs = weight * 0.45359237
    heightIncm = height * 0.3048
    return (weightInkgs / pow(heightIncm, 2))