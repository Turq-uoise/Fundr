from django.urls import path
from . import views

urlpatterns = [
  path('', views.login, name='login'),
  path('home', views.home, name='home'),
  path('explore/', views.explore, name='explore'),
  path('saved/', views.saved, name='index'),
  path('detail/', views.detail, name='detail'),
  path('accounts/signup/', views.signup, name='signup'),
  path('your_fundrs/', views.your_fundrs, name='your_fundrs'),
  path('your_fundrs/new_fundr', views.new_fundr, name='new_fundr'),


]