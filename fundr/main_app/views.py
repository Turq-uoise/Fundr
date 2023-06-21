
# Create your views here.

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .helper import *

# Create your views here.
def home(request): 
  template = is_mobile(request)
  
  return render(request, 'home.html', { 'template' : template })

def login(request, password):
  print(password)
  return redirect('accounts/login/')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}

  return render(request, 'registration/signup.html', context)

def explore(request):
  template = is_mobile(request)
  
  return render(request, 'explore.html', { 'template' : template })

def saved(request):
  template = is_mobile(request)
  
  return render(request, 'saved/index.html', { 'template' : template })

def your_fundrs(request):
  template = is_mobile(request)

  return render(request, 'your_fundrs/your_fundrs.html', {'template' : template})

def new_fundr(request):
  template = is_mobile(request)

  return render(request, 'your_fundrs/new_fundr.html', {'template' : template})

