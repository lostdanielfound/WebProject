from django.contrib import admin
from LifeFitness.models import FitnessProfile, Workout, Exercise, Workout_Session, Workout_Session_Report, Forum, Post, Post_Comment

admin.site.register(FitnessProfile)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(Workout_Session)
admin.site.register(Workout_Session_Report)
admin.site.register(Forum)
admin.site.register(Post)
admin.site.register(Post_Comment)