# https://studygyaan.com/django/how-to-extend-django-user-model
# users = User.objects.all().select_related('profile')
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth
from .forms import RegistrationForm, LoginForm, HealthForm, CreateExercise, CreateWorkout, CreateWorkoutSession 
from .models import Workout, Workout_Session, Forum, Post, Post_Comment
from django.http import HttpResponse
from datetime import datetime

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

    # Need to create a way to return only the workout sessions that are coming up 
    # and the workout session that have past after today. 
    upcomingWorkoutSessions = userWorkoutSessions.filter() # Not working, need work 
    # https://docs.djangoproject.com/en/4.1/topics/db/queries/#field-lookupsk 

    context = { 
        'weight': request.user.fitnessprofile.currentWeight, 
        'height': request.user.fitnessprofile.currentheight,
        'BMI': request.user.fitnessprofile.BMI,
        'goal': request.user.fitnessprofile.goalWeight,
        'userWorkoutSessions': userWorkoutSessions,
    }

    return render(request, 'LifeFitness/account.html', context=context)

def createWorkoutSession(request, workoutlistID = -1):

    if not request.user.is_authenticated: # If user isn't authenticated
        return redirect('/login')

    if request.method == "POST":
        workoutlistID = request.POST.get("ID", "")
        currentWorkoutSession = Workout_Session.objects.get(pk=workoutlistID) 
        currentWorkoutSession.name = request.POST.get("Name", "") # Set the name
        currentWorkoutSession.date = datetime.strptime(request.POST.get("Date", ""), "%m/%d/%Y") # Set the date

        currentWorkoutSession.save() 

        return redirect('/account')
    elif request.method == "GET":
        if workoutlistID == -1:
            newWorkoutSession = Workout_Session()
            newWorkoutSession.name = "" # default inital name
            newWorkoutSession.date = datetime(2000, 1, 1) # default date
            newWorkoutSession.fitnesuser = request.user
            newWorkoutSession.save()

            context = {
                'ID': newWorkoutSession.pk,
                'workoutlist': newWorkoutSession.workoutList.all(), 
                'form': CreateWorkoutSession(),
            }
        else: 
            currentWorkoutSession = Workout_Session.objects.get(pk=workoutlistID) # get the current workout_session

            context = {
                'ID': currentWorkoutSession.pk,
                'workoutlist': currentWorkoutSession.workoutList.all(),
                'form': CreateWorkoutSession(),
            }

    return render(request, 'LifeFitness/createworkoutsession.html', context=context)

def createWorkout(request, workoutlistID):
    
    if not request.user.is_authenticated: # If user isn't authenticated
        return redirect('/login')

    if request.method == "POST":
        # Take in the POST request and create a workout to add it to 
        # the Workout_session of pk = workoutlistID 
        newWorkout = CreateWorkout(request.POST)
        if newWorkout.is_valid(): 
           newWorkout.save(workoutlistID=workoutlistID)
           return redirect('/account/createworkoutsession/' + str(workoutlistID))


    context = {
        'form': CreateWorkout(),
        'ID': workoutlistID, 
    }
    
    return render(request, 'LifeFitness/createworkout.html', context=context)

def forums(request):

    context = {
        'Forums':  Forum.objects.all()
    }

    return render(request, 'LifeFitness/forum.html', context=context)

def posts_page(request, forumID):

    Forum_list = Forum.objects.get(pk=forumID)
    
    context = {
        'forum_list': Forum_list,
    }

    return render(request, 'LifeFitness/posts_page.html', context=context)
    
def post(request, postID):
    
    if not request.user.is_authenticated: # if user isn't authenticated then it should be anonymous
        user_name = "Anonymous"
    user_name = request.user.username

    post = Post.objects.get(pk=postID) 

    context = {
        'post': post,
    }

    return render(request, 'LifeFitness/post.html', context=context)
