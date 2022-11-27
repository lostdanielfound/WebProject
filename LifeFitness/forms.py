# Form guide: https://ordinarycoders.com/django-custom-user-profile#Creating%20a%20user%20page
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from LifeFitness.models import FitnessProfile, Exercise, Workout
from django import forms
from LifeFitness.helpfunctions import convertBMI, CompleteExerciseList

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
        current_user.fitnessprofile.BMI = convertBMI(curweight, curheight)
        current_user.fitnessprofile.goalWeight = self.cleaned_data['goalWeight']
        current_user.fitnessprofile.save()

class LoginForm(forms.Form):
    Username = forms.CharField(label="Username", max_length=200)
    Password = forms.CharField(label="Password", max_length=200)
 
class CreateExercise(forms.Form):
    Name = forms.CharField(label="Exercise name", max_length=100)

    def save(self):
        newExercise = Exercise()
        newExercise.name = self.cleaned_data['Name']
        newExercise.save() 

class CreateWorkout(forms.Form):
    Exercise = 
    RepCount = forms.IntegerField(label="Rep Count", max_value=100, min_value=0)
    SetCount = forms.IntegerField(label="Set Count", max_value=100, min_value=0)

class CreateWorkoutSession(forms.Form):
    Name = forms.CharField(label="Session Name", help_text="Session Name")
    Date = forms.DateField(label="Workout Date", widget=forms.DateInput()) 
    Exlist = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=CompleteExerciseList())

    def save(self):
        newWorkout = Workout()
        newWorkout.name = self.cleaned_data['Name']
        newWorkout.Date = self.cleaned_data['Date']
        newWorkout.save() # Save the workout before adding exercises

        # Now add the workout list
        for exercise in self.cleaned_data['Exlist']: 
            newWorkout.exerciseList.add(exercise)
        newWorkout.save()

class PostWorkoutReport(forms.Form):
    ...
# https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django

# widgets: https://docs.djangoproject.com/en/4.1/ref/forms/widgets/#django.forms.TextInput