# Form guide: https://ordinarycoders.com/django-custom-user-profile#Creating%20a%20user%20page
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from LifeFitness.models import FitnessProfile
from django import forms

class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2')
    
    def save(self, commit=True): 
        user = super().save(commit=False)
        if commit: 
            user.save() 
        return user

class HealthForm(forms.Form):

    class Meta:
        model = FitnessProfile
        fields = ('currentheight', 'currentWeight', 'BMI', 'goalWeight')

    def save(self, request):
        fit_user = FitnessProfile
        fit_user.currentheight = self.cleaned_data['currentheight']
        fit_user.currentWeight = self.cleaned_data['currentWeight']
        fit_user.BMI = self.cleaned_data['BMI']
        fit_user.goalWeight = self.cleaned_data['goalWeight']
        fit_user.fitnessUser = request.user

class LoginForm(forms.Form):
    Username = forms.CharField(label="Username", max_length=200)
    Password = forms.CharField(label="Password", max_length=200)