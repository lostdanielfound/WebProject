from django.shortcuts import render, redirect
from django.contrib import auth
from LifeFitness.models import FitnessProfile
from LifeFitness.forms import CreateUserForm, FitnessUserForm, FitnessProfileForm, LoginForm
from django.http import HttpResponse

def home(request):
    return render(request, 'LifeFitness/homepage.html')

def fitnessuserpage(request):
    user_form = FitnessUserForm(instance=request.user)
    profile_form = FitnessProfileForm(instance=request.user.fitnessprofileform)

def account(request):
    # user form that is based off the attributes from FitnessUser model
    fitnessuser_form = FitnessUserForm(instance=request.fitnessuser)

    # profile form that is based off the attributes from Fi
    fitnessprofile_form = FitnessProfileForm(instance=request.user.fitnessprofile)

    context = {
        "fitnessuser": request.fitnessuser, 
        "fitnessuser_form": fitnessuser_form, 
        "fitnessprofile_form": fitnessprofile_form
    }
    return render(request, 'LifeFitness/account.html', context=context)

def login(request):

    #If user sumbitted post request
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

    Title = 'LifeFitness | Account'
    form = LoginForm()

    context = {
        "Title": Title, 
        "form": form
    }

    return render(request, 'LifeFitness/login.html', context=context)

def signup(request): 
    if request.POST == 'POST':
        form = CreateUserForm()
        if form.is_valid():
            form.save()
    else:
        form = CreateUserForm()

    context = {
        'form': form
    }
    return render(request, 'LifeFitness/signup.html', context=context)

