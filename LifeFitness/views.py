from pyexpat.errors import messages
from django.shortcuts import render
from LifeFitness.forms import CreateUserForm, FitnessUserForm, FitnessProfileForm
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
    context = {}
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

