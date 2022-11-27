# Database Models for Webapplication: LifeFitness
from django.db import models 
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class FitnessProfile(models.Model): 
    currentheight = models.IntegerField(default=0) # current height of the fitness user
    currentWeight = models.IntegerField(default=0) # current weight of the fitness user
    BMI = models.IntegerField(default=0) # BMI score of the fitness user
    goalWeight = models.IntegerField(default=0) # goal weight the fitness user wants to reach
    
    # FitnessUser is an inheritance User model, will inheriant username, password, etc attributes. 
    fitnessUser = models.OneToOneField(User, on_delete=models.CASCADE) 

    def __str__(self):
        return(self.fitnessUser.username + " (" + str(self.pk) + ")") 
    # Upon User model is created,
    # function is called to create connection between the saved User 
    # object and FitnessUser
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            FitnessProfile.objects.create(fitnessUser = instance)
    
    # Upon User model is saved, updates to the FitnessUser is 
    # saved by function. 
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.fitnessprofile.save()
        

class Exercise(models.Model): 
    name = models.CharField(max_length=200, default="default_value") # name of the exercise

    def __str__(self):
        return(self.name)

class Workout(models.Model):
    exerciseName = models.ForeignKey(Exercise, on_delete=models.CASCADE) # name of the exercise
    repCount = models.IntegerField(default=0) # number of complete reps per set in a workout
    setCount = models.IntegerField(default=0) # number of sets user will do during a workout

    def __str__(self):
        return(self.name + " (" + str(self.pk) + ")" + " [" + str(self.setCount) + " ," + str(self.repCount) + "]" )

class Workout_Session(models.Model):
    name = models.CharField(max_length=200,blank=True) # name of workout, not required
    date = models.DateField(auto_now=True) # Set Date to start the workout 
    exerciseList = models.ManyToManyField(Workout) # List of Exercises for the workout
    fitnesuser = models.ForeignKey(User, on_delete=models.CASCADE) # User and workout connection, User can have multiple Workouts 

    def __str__(self):
        if self.name == "":
            return("Workout object (" + str(self.pk) + ")")
        return(self.name + " (" + str(self.pk) + ")")

class Workout_Session_Report(models.Model):
    self_report = models.TextField(blank=True, max_length=300) # Self report on how the workout felt and overall experience 
    duration = models.TimeField(auto_now=False, auto_now_add=False) # total duration of the workout
    workoutID = models.OneToOneField(Workout_Session, on_delete=models.CASCADE) # One-to-one relationship between the workout and report

    def __str__(self):
        return("Report object (" + str(self.pk) + ") -> " + self.workoutID.__str__())