# https://studygyaan.com/django/how-to-extend-django-user-model
# users = User.objects.all().select_related('profile')
from django.shortcuts import render, redirect
from django.contrib import auth
from LifeFitness.models import FitnessProfile
from LifeFitness.forms import RegistrationForm, LoginForm, HealthForm
from django.http import HttpResponse

def home(request):
    return render(request, 'LifeFitness/homepage.html', context={ request.user: 'user'})

def login(request):
    if(request.method == "POST"):
        form = LoginForm(request.POST)
        if form.is_valid(): # Check to see if form is vaild from POST 
            username = form.cleaned_data['Username']
            password = form.cleaned_data['Password']
            user = auth.authenticate(request, username=username, password=password)
            
            #Check to see if the user does exist
            if user is not None: 
                print('Successful Login')
                auth.login(request, user)
                return redirect('/')
            else:
                print('Unsuccessful login!')
                return redirect('/')

    form = LoginForm()

    context = {
        "form": form
    }

    return render(request, 'LifeFitness/login.html', context=context)

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/') #redirects user back to homepage

def healthsignup(request): 
    if request.methed == "POST":
        health_form = HealthForm(request.POST)
    else:
        health_form = HealthForm()

    # Once user comes to this page, they should be logged in 
    # we can setup the onetoone healthForm that way thorugh request.user
    context = {
        'health_form': HealthForm,
    }
    
    return render(request, '/healthsignup')

def signup(request): 
    if request.method == "POST":
        Registration_form = RegistrationForm(request.POST)
        if Registration_form.is_valid():
            # Getting the user back to login user
            user = Registration_form.save() # save the fitness profile of the user
            print('Successfully sign up')

            auth.login(request, user) # login User
            print('Successful login')

            return healthsignup(request)
        else: 
            # Should redirect the user back to the sign up 
            # screen to try to reenter their data again. 
            print('Unsuccessfully data entry')
            return redirect('/signup')
    else:
        Registration_form = RegistrationForm()

    context = {
        'Registration_form': Registration_form,
    }
    return render(request, 'LifeFitness/signup.html', context=context)

def account(request):

    # IF the user has not Logged in yet, they should be sent 
    # to the login page to login. 
    # Else they should be greated with they Profile info.
    # Read https://docs.djangoproject.com/en/4.1/ref/request-response/ for request attribute details

    if not request.user.is_authenticated: 
        return redirect('/login')

    # user form that is based off the attributes from FitnessUser model
    # fitnessuser_form = FitnessUserForm(instance=request.fitnessuser)

    # profile form that is based off the attributes from Fi
    # fitnessprofile_form = FitnessProfileForm(instance=request.user.fitnessprofile)

    context = {
        "user": request.user
    }
    return render(request, 'LifeFitness/account.html', context=context)
