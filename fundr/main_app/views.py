
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login as login_process
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import *
from django.http import JsonResponse
import json

from django.core import serializers
from .models import Fundraiser, Post, Profile
from .helper import *
import pgeocode
import numpy as np


# Create your views here.
def home(request): 
  if (request.user.is_authenticated != True):
    return redirect('/accounts/login/')
  
  template = is_mobile(request)
  return render(request, 'home.html', { 'template' : template })

def login(request):
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
      print(request.POST)
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
  if (request.user.is_authenticated != True):
    return redirect('/accounts/login/')
  

  template = is_mobile(request)
  
  user = Profile.objects.get(user_id=request.user.id)
  user_location = np.array([[user.latitude, user.longitude]])
  fundrs = Fundraiser.objects.all()
  
  for fundr in fundrs:
    fundr_location = np.array([[fundr.lat, fundr.long]])
    distance = pgeocode.haversine_distance(fundr_location, user_location)
    floats = [float(np_float) for np_float in distance]
    fundr.distance_from_user = floats[0]
    fundr.save()

  fundrs = Fundraiser.objects.all().order_by('distance_from_user')

  serialized_fundrs = serializers.serialize('json', fundrs)
  return render(request, 'explore.html', { 'template' : template, 'fundrs': json.dumps(serialized_fundrs) })

def saved(request):
  if (request.user.is_authenticated != True):
    return redirect('/accounts/login/')
  
  template = is_mobile(request)
  
  return render(request, 'saved/index.html', { 'template' : template })

def detail(request, fundr_id):
  if (request.user.is_authenticated != True):
    return redirect('/accounts/login/')
  
  template = is_mobile(request)

  fundr = Fundraiser.objects.id(id=fundr_id)
  return render(request, 'detail.html', { 'template' : template, 'fundrs': fundr })



def your_fundrs(request):
  if (request.user.is_authenticated != True):
    return redirect('/accounts/login/')
  
  template = is_mobile(request)
  fundrs = Fundraiser.objects.filter(owner_id=request.user.id)
  print(type(fundrs))
  return render(request, 'fundrs/your_fundrs.html', { 'template' : template, 'fundrs': fundrs })

def store_user_location(request):
  print(request.user)
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
      print('saved??')
      return JsonResponse({'message': 'Location stored successfully'})
    else:
        print('User not authenticated')
        return JsonResponse({'error': 'User not authenticated'}, status=401)
  else:
    print('Invalid request method')  
    return JsonResponse({'error': 'Invalid request method'})

class FundrCreate(CreateView):
  
  
  model = Fundraiser
  form_class= FundrForm
  success_url = '/your_fundrs'
  template_name = 'fundrs/new_fundr.html'
  def get(self, request, *args, **kwargs):
    # Access the request object here
    # You can perform any necessary operations with the request
    self.request = request
    if (request.user.is_authenticated != True):
      return redirect('/accounts/login/')
    # Call the parent class's get() method to handle form-related logic
    return super().get(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    template = is_mobile(self.request)
    context['template'] = template
    # Access the request object through self.request here
    # You can add additional context variables based on the request

    return context
  
  def form_valid(self, form):
    # Access the user and add it to the model entry
    nomi = pgeocode.Nominatim('gb')
    post_code = formatPostcode(form.instance.location).upper()
    form.instance.lat = nomi.query_postal_code(post_code).latitude
    form.instance.long = nomi.query_postal_code(post_code).longitude
    form.instance.owner = self.request.user.profile
    return super().form_valid(form)

def fundrs_detail(request, fundr_id):
  template = is_mobile(request)
  fundr = Fundraiser.objects.get(id=fundr_id)
  nomi = pgeocode.Nominatim('gb')
  post_code = formatPostcode(fundr.location).upper()
  print(post_code)
  placename = nomi.query_postal_code(post_code).place_name
  print(placename)
  return render(request, 'fundrs/detail.html', {
    'fundr': fundr,
    'template' : template,
    'placename': placename,
  })


  
