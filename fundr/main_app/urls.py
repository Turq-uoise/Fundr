from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('explore/', views.explore, name='explore'),
  path('saved/', views.saved, name='index'),
  path('accounts/signup/', views.signup, name='signup'),
]