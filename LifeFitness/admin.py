from django.contrib import admin
from LifeFitness.models import FitnessProfile, Workout, Exercise, Workout_Session, Workout_Session_Report

admin.site.register(FitnessProfile)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(Workout_Session)
admin.site.register(Workout_Session_Report)
