
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login as login_process
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import *


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
      print(request.POST)
      # This is how we log a user in via code
      login_process(request, user)
      #get avatar and associate avatar:
      # def assoc_avatar(request, user_id):
      #   avatar = request.POST.get("avatar", "")
      #   Profile.objects.get(user_id=user_id).avatar.add(avatar)
      # assoc_avatar(request, user_id)
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
  return render(request, 'explore.html', { 'template' : template })

def saved(request):
  template = is_mobile(request)
  return render(request, 'saved/index.html', { 'template' : template })

def detail(request, fundr_id):
  template = is_mobile(request)
  fundr = Fundraiser.objects.id(id=fundr_id)
  return render(request, 'detail.html', { 'template' : template, 'fundrs': fundr })

def detail(request, fundr_id):
  mobile = is_mobile(request)
  if mobile:
     template = 'base.html'
  else:
     template = 'base-desktop.html'

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

  return render(request, 'your_fundrs/new_fundr.html', { 'template' : template, })