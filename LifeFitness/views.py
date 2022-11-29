# https://studygyaan.com/django/how-to-extend-django-user-model
# users = User.objects.all().select_related('profile')
from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import RegistrationForm, LoginForm, HealthForm, CreateExercise, CreateWorkout, CreateWorkoutSession 
from django.http import HttpResponse
from math import pow

def home(request):
    return render(request, 'LifeFitness/homepage.html', context={ request.user: 'user'})

def login(request):
    # POST REQUEST
    if(request.method == "POST"):
        form = LoginForm(request.POST) 
        if form.is_valid(): 
            # Attempt to Authenticate the User
            username = form.cleaned_data['Username']
            password = form.cleaned_data['Password']
            user = auth.authenticate(request, username=username, password=password)
            
            # Check to see if the user does exist
            if user is not None:
                auth.login(request, user)
                if user.is_authenticated: 
                    print('* SUCCESSFUL Login of User *: ' + user.get_username())
                    return redirect('/')
                else: 
                    print('* FAILED Could not log User *: ' + user.get_username()) # This should never run because is_authenticated is true always
            else:
                print('~ FAILED User does not exist ~: ' + username)
                return redirect('/login')

    # GET REQUEST
    form = LoginForm() 
    return render(request, 'LifeFitness/login.html', context={"form": form})

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request) # Logs User out of current session
        return redirect('/') # redirects user back to homepage
    else: 
        return redirect('/') # This shouldn't ever run since logout button isn't available to users who are not logged in.

def healthsignup(request): 
    if request.method == "POST":
        health_form = HealthForm(request.POST)
        if health_form.is_valid():
            current_user = request.user
            health_form.save(current_user)
            return redirect('/account')
        else: 
            # Should redirect the user back to the sign up 
            # screen to try to reenter their data again. 
            print('Unsuccessfully data entry')
            default_error = 'Unsuccessful data entry, please try again'
            context = {
                'default_error': default_error 
            }

            return render(request, 'LifeFitness/healthsignup.html', context=context)
    else:
        health_form = HealthForm()

    # Once user comes to this page, they should be logged in 
    # we can setup the onetoone healthForm that way through request.user    
    return render(request, 'LifeFitness/healthsignup.html', context={'health_form': health_form})

def signup(request): 
    if request.method == "POST":
        Registration_form = RegistrationForm(request.POST)
        if Registration_form.is_valid():
            # Getting the user back to login user
            user = Registration_form.save() # Creates User account and returns User
            print('* SUCCESSFUL sign up *')

            auth.login(request, user) # login User
            if user.is_authenticated: 
                print('* SUCCESSFUL Login of User *: ' + user.get_username())
            else: 
                print('* FAILED Could not log User *: ' + user.get_username()) # This should never run because is_authenticated is true always

            return redirect('/healthsignup')
        else: 
            # Should redirect the user back to the sign up 
            # screen to try to reenter their data again. 
            print('Unsuccessfully data entry')
            return redirect('/signup')
    else:
        Registration_form = RegistrationForm()

    return render(request, 'LifeFitness/signup.html', context={'Registration_form': Registration_form})

def account(request):
    # IF the user has not Logged in yet, they should be sent 
    # to the login page to login. 
    # Else they should be greated with they Profile info.
    # Read https://docs.djangoproject.com/en/4.1/ref/request-response/ for request attribute details

    if not request.user.is_authenticated: 
        return redirect('/login')
   
    if request.method == "POST":
        exerciseform = CreateExercise(request.POST)
        workoutform = CreateWorkout(request.POST)
         
        if exerciseform.is_valid():
            exerciseform.save() # Create the new exercise
            workoutform = CreateWorkout() # Fresh workout form after exercise creation        
            print('* SUCCESSFUL exercise creation *')
        elif workoutform.is_valid():
            print(request.POST)
            workoutform.save() # Create the new workout session 
            exerciseform = CreateExercise() # Fresh workout form after Workout Creation
            print('* SUCCESSFULY workout creation *')

    userWorkoutSessions = request.user.workout_session_set.all()

    context = { 
        'weight': request.user.fitnessprofile.currentWeight, 
        'height': request.user.fitnessprofile.currentheight,
        'BMI': request.user.fitnessprofile.BMI,
        'goal': request.user.fitnessprofile.goalWeight,
        'userWorkoutSessions': userWorkoutSessions,
    }

    return render(request, 'LifeFitness/account.html', context=context)

def createWorkoutSession(request):

    context = {
        'form': CreateWorkoutSession(),
    }

    return render(request, 'LifeFitness/createworkoutsession.html', context=context)