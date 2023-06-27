
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login as login_process
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django import forms
from django.core.files.uploadedfile import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import *
from .models import Fundraiser, Post, Profile
from .helper import *
from PIL import *

import json
import pgeocode
import numpy as np
import datetime
import uuid
import boto3
import os
import datetime
from ukpostcodeutils import validation

# Create your views here.
def home(request): 
  if (request.user.is_authenticated != True): return redirect('/accounts/login/')
  template = is_mobile(request)

  user = request.user
  
  posts = []
  fundrs = User.objects.get(id=request.user.id).fundraiser_set.all()

  for fundr in fundrs:
    post_list = list(Post.objects.filter(fundraiser=fundr.id))
    posts.extend(post_list)

  sorted_list = list(reversed(sorted(posts, key=lambda x: x.date_created)))
  page = request.GET.get('page', 1)
  paginator = Paginator(sorted_list, 3)

  try:
      posts = paginator.page(page)
  except PageNotAnInteger:
      posts  = paginator.page(1)
  except EmptyPage:
      posts = paginator.page(paginator.num_pages)

  return render(request, 'home.html', { 'template' : template, 'posts': posts, 'title': 'Home', 'user': user })


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

  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  
  context = {'form': form, 'error_message': error_message, 'title': 'Sign-up'}

  return render(request, 'registration/signup.html', context)


def explore(request):
  if (request.user.is_authenticated != True): return redirect('/accounts/login/')
  template = is_mobile(request)

  if request.method == 'POST':
    fundr_id = request.POST.get("fundr_id")
    current_index = int(request.POST.get("current_index"))
    Fundraiser.objects.get(id=fundr_id).followers.add(request.user)

  else: 
    current_index = 0

  user = Profile.objects.get(user_id=request.user.id)
  user_location = np.array([[user.latitude, user.longitude]])
  fundrs = Fundraiser.objects.all()
  
  for fundr in fundrs:
    fundr_location = np.array([[fundr.lat, fundr.long]])
    distance = np.round(pgeocode.haversine_distance(fundr_location, user_location),1)
    floats = [float(np_float) for np_float in distance]
    fundr.distance_from_user = floats[0]
    fundr.save()
  
  fundrs = Fundraiser.objects.filter(distance_from_user__lte=user.catchment)
  fundrs = fundrs.order_by('distance_from_user','id')
  fundrs = fundrs[current_index:]

  serialized_fundrs = serializers.serialize('json', fundrs)
  return render(request, 'explore.html', { 'template' : template, 'fundrs': json.dumps(serialized_fundrs), "current_index": current_index, 'title': 'Explore', 'fundr_list': fundrs })


def following(request):
  if (request.user.is_authenticated != True): return redirect('/accounts/login/')
  template = is_mobile(request)

  fundrs = User.objects.get(id=request.user.id).fundraiser_set.all()
  
  return render(request, 'following/index.html', { 'template' : template, 'fundrs': fundrs, 'title': 'Following' })


def your_fundrs(request):
  if (request.user.is_authenticated != True): return redirect('/accounts/login/')
  
  template = is_mobile(request)

  fundrs = Fundraiser.objects.filter(owner_id=request.user.id)
  return render(request, 'fundrs/your_fundrs.html', { 'template' : template, 'fundrs': fundrs, 'title': 'Your Fundrs' })


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
    
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)
    
  else:
    return JsonResponse({'error': 'Invalid request method'})


class FundrCreate(CreateView):
  model = Fundraiser
  form_class= FundrForm
  # success_url = '/your_fundrs'
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
    nomi = pgeocode.Nominatim('gb')
    post_code = formatPostcode(form.instance.location).upper()
    form.instance.lat = nomi.query_postal_code(post_code).latitude
    form.instance.long = nomi.query_postal_code(post_code).longitude
    form.instance.owner = self.request.user.profile
    fundr_photo_file = self.request.FILES.get('image')

    if not validation.is_valid_postcode(post_code.replace(' ', '')):
      messages.error(self.request, 'Not a valid postcode')
      return redirect('/your_fundrs/new_fundr')
    
    if form.instance.goal < 100 or form.instance.goal > 100000:
      messages.error(self.request, 'Goals can be between £100 and £100,000')
      return redirect('/your_fundrs/new_fundr')

    if fundr_photo_file:
        # Upload the image to S3
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + fundr_photo_file.name[fundr_photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(fundr_photo_file, bucket, key)
            image_url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            form.instance.image = image_url
        except Exception as e:
            print('An error occurred uploading file to S3:', str(e))

    return super().form_valid(form)
  

class FundrUpdate(UpdateView):
  model = Fundraiser
  form_class = FundrForm
  template_name = 'fundrs/new_fundr.html'

  def get(self, request, *args, **kwargs):
    # Access the request object here
    # You can perform any necessary operations with the request
    self.request = request

    if (request.user.is_authenticated != True):
      return redirect('/accounts/login/')
    
    f = Fundraiser.objects.get(id=kwargs.get('pk'))
    if (self.request.user.profile != f.owner):
      return redirect('/home')
    
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
    post_code = form.instance.location.strip(' ')
    id = self.kwargs.get('pk')

    if not validation.is_valid_postcode(post_code):
      messages.error(self.request, 'Not a valid postcode')
      return redirect('/fundrs/{}/update'.format(id))
    
    if form.instance.goal < 100 or form.instance.goal > 100000:
      messages.error(self.request, 'Goals can be between £100 and £100,000')
      return redirect('/fundrs/{}/update'.format(id))
    
    return super().form_valid(form)
  

class FundrDelete(DeleteView):
  model = Fundraiser
  success_url = '/your_fundrs/'


def fundrs_detail(request, fundr_id):
  template = is_mobile(request)
  following = False
  fundr = Fundraiser.objects.get(id=fundr_id)

  if (fundr.followers.filter(id=request.user.id).exists()):
    following = True

  if request.method == 'POST':
    fundr_id = request.POST.get('fundr_id')

    if following == True:
      Fundraiser.objects.get(id=fundr_id).followers.remove(request.user)
      following = False

    else:
      Fundraiser.objects.get(id=fundr_id).followers.add(request.user)
      following = True

  nomi = pgeocode.Nominatim('gb')
  post_code = formatPostcode(fundr.location).upper()
  placename = nomi.query_postal_code(post_code).place_name
  post_form = PostForm()
  user = request.user
  fundr_posts = Post.objects.filter(fundraiser_id=fundr_id)

  return render(request, 'fundrs/detail.html', {
    'fundr': fundr,
    'template' : template,
    'placename': placename,
    'post_form': post_form,
    'user': user,
    'posts': fundr_posts,
    'following': following,
    'title': 'Details',
  })


def add_post(request, fundr_id):
  if (request.user.is_authenticated != True): return redirect('/accounts/login/')
  # get the form:
  form = PostForm(request.POST)
  # get the image:
  post_photo_file = request.FILES.get('image', None)

  # check form is valid:
  if form.is_valid():
    # do the amazon s3 upload:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + post_photo_file.name[post_photo_file.name.rfind('.'):]
    print(s3)
    print(key)
    print(form.errors)
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(post_photo_file, bucket, key)
      # this is the uploaded url of the image:
      image_url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      # Create the new post object with the form data
      new_post = Post.objects.create(
          title=form.cleaned_data['title'],
          content=form.cleaned_data['content'],
          image=image_url,
          owner_id=form.cleaned_data['owner'],
          fundraiser_id=form.cleaned_data['fundraiser'],
          date_created=datetime.date.today()
        )
      
    except:
      new_post = Post.objects.create(
          title=form.cleaned_data['title'],
          content=form.cleaned_data['content'],
          owner_id=form.cleaned_data['owner'],
          fundraiser_id=form.cleaned_data['fundraiser'],
          date_created=datetime.date.today()
        )
      print('An error occurred uploading file to S3')

  return redirect('detail', fundr_id=fundr_id)


def delete_post(request, post_id, fundr_id):
  if (request.user.is_authenticated != True): return redirect('/accounts/login/')

  post = Post.objects.get(pk=post_id)
  post.delete()

  return redirect('detail', fundr_id=fundr_id)


def login(request):
  return redirect('accounts/login/', {'title': 'Login'})


def about(request):
  template = is_mobile(request)
  return render(request, 'about.html', { 'template' : template, 'title': 'About'})


def contact(request):
  template = is_mobile(request)
  return render(request, 'contact.html', { 'template' : template, 'title': 'Contact Us'})


def terms(request):
  template = is_mobile(request)
  return render(request, 'terms.html', { 'template' : template, 'title': 'Terms & Conditions and Privacy Policy'})


class SettingsView(TemplateView):
  template_name = 'settings.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    template = is_mobile(self.request)
    context['template'] = template

    return context


class SettingsUpdate(UpdateView):
  model = Profile
  form_class = SettingsForm
  success_url = '/settings'

  def form_valid(self, form):
    messages.success(self.request, 'Your catchment range has been updated')
    
    return super().form_valid(form)


def add_avatar(request, fundr_id):
  if (request.user.is_authenticated != True): return redirect('/accounts/login/')
  # get the form:
  
  form = AvatarForm(request.POST)
  # get the image:
  post_photo_file = request.FILES.get('avatar', None)
  # check form is valid:
  if form.is_valid():
    # do the amazon s3 upload:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + post_photo_file.name[post_photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(post_photo_file, bucket, key)
      # this is the uploaded url of the image:
      image_url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      # Create the new post object with the form data
      new_post = Post.objects.create(
          avatar=image_url
        )
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', fundr_id=fundr_id)


    
