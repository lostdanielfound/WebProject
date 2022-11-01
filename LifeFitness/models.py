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
    