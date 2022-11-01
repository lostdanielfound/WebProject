# Form guide: https://ordinarycoders.com/django-custom-user-profile#Creating%20a%20user%20page
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from LifeFitness.models import FitnessProfile
from django import forms

class CreateUserForm(UserCreationForm):
    ...

class FitnessUserForm(forms.ModelForm):

    # Since we are inherianting from forms.ModelForm
    # We can create a form based off of the User model
    # within Meta class
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class FitnessProfileForm(forms.ModelForm):
    class Meta:
        model = FitnessProfile
        fields = ('currentheight', 'currentWeight', 'BMI', 'goalWeight')

class LoginForm(forms.Form):
    Username = forms.CharField(label="Username", max_length=200)
    Password = forms.CharField(label="Password", max_length=200)