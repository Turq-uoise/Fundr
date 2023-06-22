
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login as login_process
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import json

from .forms import ProfileForm, FundrForm

from .models import Fundraiser, Post, Profile
from .helper import *

# Create your views here.
def home(request): 
  mobile = is_mobile(request)
  if mobile:
     template = 'base.html'
  else:
     template = 'base-desktop.html'
  
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
      login_process(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
      print(error_message)
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  
  context = {'form': form, 'error_message': error_message}

  return render(request, 'registration/signup.html', context)

def explore(request):
  mobile = is_mobile(request)
  if mobile:
     template = 'base.html'
  else:
     template = 'base-desktop.html'
  return render(request, 'explore.html', { 'template' : template })

def saved(request):
  template = is_mobile(request)
  
  return render(request, 'saved/index.html', { 'template' : template })

def detail(request, fundr_id):
  mobile = is_mobile(request)
  if mobile:
     template = 'base.html'
  else:
     template = 'base-desktop.html'

  fundr = Fundraiser.objects.id(id=fundr_id)
  return render(request, 'detail.html', { 'template' : template, 'fundrs': fundr })

def your_fundrs(request):
  mobile = is_mobile(request)
  if mobile:
     template = 'base.html'
  else:
     template = 'base-desktop.html'

  return render(request, 'your_fundrs/your_fundrs.html', { 'template' : template, })

def new_fundr(request):
  mobile = is_mobile(request)
  if mobile:
     template = 'base.html'
  else:
     template = 'base-desktop.html'

  return render(request, 'your_fundrs/new_fundr.html', { 'template' : template, })

def store_user_location(request):
  if request.method == 'POST':
    if request.user.is_authenticated:
      #Convert the raw HttpRequest body bytestring into a python dict:
      req_params = json.loads(request.body.decode('utf-8'))
      #Store the user idea of the authenticated user:
      req_user_id = request.user.id
      #Store the lat and lon variables:
      latitude = req_params["userlat"]
      longitude = req_params["userlon"]
      #Get the correct profile object:
      profile_to_update = Profile.objects.get(user_id=req_user_id)
      #Update the profile object:
      profile_to_update.latitude = latitude
      profile_to_update.longitude = longitude
      profile_to_update.save()
      return JsonResponse({'message': 'Location stored successfully'})
    return JsonResponse({'error': 'Invalid request method'})