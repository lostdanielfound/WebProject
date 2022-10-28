from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'LifeFitness/homepage.html')

def login(request):
    context = {}
    return render(request, 'LifeFitness/login.html', context=context)

def signup(request): 
    context = {}
    return render(request, 'LifeFitness/signup.html', context=context)

