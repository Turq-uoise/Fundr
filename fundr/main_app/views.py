
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
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import *

from .models import *
from .models import Fundraiser, Post, Profile
from .helper import *

# Create your views here.
def home(request): 
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
  template = is_mobile(request)
  
  fundrs = Fundraiser.objects.all()
  serialized_fundrs = serializers.serialize('json', fundrs)
  return render(request, 'explore.html', { 'template' : template, 'fundrs': json.dumps(serialized_fundrs) })

def saved(request):
  template = is_mobile(request)
  
  return render(request, 'saved/index.html', { 'template' : template })

def detail(request, fundr_id):
  template = is_mobile(request)

  fundr = Fundraiser.objects.id(id=fundr_id)
  return render(request, 'detail.html', { 'template' : template, 'fundrs': fundr })



def your_fundrs(request):
  template = is_mobile(request)
  fundrs = Fundraiser.objects.filter(owner_id=request.user.id)
  print(type(fundrs))
  return render(request, 'your_fundrs/your_fundrs.html', { 'template' : template, 'fundrs': fundrs })

class FundrCreate(CreateView):
  
  model = Fundraiser
  form_class= FundrForm
  success_url = '/your_fundrs'
  template_name = 'your_fundrs/new_fundr.html'
  def get(self, request, *args, **kwargs):
      # Access the request object here
      # You can perform any necessary operations with the request
      self.request = request
      # Call the parent class's get() method to handle form-related logic
      return super().get(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      template = is_mobile(self.request)
      context['template'] = template
      # Access the request object through self.request here
      # You can add additional context variables based on the request

      return context

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