# Form guide: https://ordinarycoders.com/django-custom-user-profile#Creating%20a%20user%20page
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from LifeFitness.models import FitnessProfile
from django import forms
from math import pow

class RegistrationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2')
    
    def save(self, commit=True): 
        user = super().save(commit=False)
        if commit: 
            user.save() 
        return user # return user to login under successfully creation 

class HealthForm(forms.ModelForm):

    class Meta:
        model = FitnessProfile
        fields = ['currentheight', 'currentWeight', 'goalWeight']

    # Save all changes to the Current_user's fitnessprofile. 
    def save(self, current_user):
        curheight = self.cleaned_data['currentheight']
        curweight = self.cleaned_data['currentWeight']

        current_user.fitnessprofile.currentheight = curheight
        current_user.fitnessprofile.currentWeight = curweight
        current_user.fitnessprofile.BMI = ((curweight * 0.45359237) / pow(curheight * 0.3048, 2))
        current_user.fitnessprofile.goalWeight = self.cleaned_data['goalWeight']
        current_user.fitnessprofile.save()

class LoginForm(forms.Form):
    Username = forms.CharField(label="Username", max_length=200)
    Password = forms.CharField(label="Password", max_length=200)

class CreateExercise(forms.Form):
    Name = forms.CharField(label="Exercise name", max_length=100)
    Description = forms.CharField(label="Description of workout", widget=forms.Textarea, max_length=400)
    RepCount = forms.IntegerField(label="Rep Count", max_value=100, min_value=0)
    SetCount = forms.IntegerField(label="Set Count", max_value=100, min_value=0)
    
class CreateWorkout(forms.Form):
    Date_And_Time = forms.DateTimeField(widget=forms.DateTimeInput)


# https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django

