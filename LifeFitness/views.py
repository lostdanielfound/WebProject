from pyexpat.errors import messages
from django.shortcuts import render
from LifeFitness.forms import CreateUserForm
from django.http import HttpResponse

def home(request):
    return render(request, 'LifeFitness/homepage.html')

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

