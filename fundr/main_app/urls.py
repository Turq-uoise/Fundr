from django.urls import path
from . import views

urlpatterns = [
  path('', views.login, name='login'),
  path('home', views.home, name='home'),
  path('explore/', views.explore, name='explore'),
  path('explore/<int:fundr_id>/save_fundr/<int:user_id', views.save_fundr, name='save_fundr'),
  path('saved/', views.saved, name='index'),
  path('detail/', views.detail, name='detail'),
  path('accounts/signup/', views.signup, name='signup'),
  path('your_fundrs/', views.your_fundrs, name='your_fundrs'),
  path('your_fundrs/new_fundr', views.FundrCreate.as_view(), name='new_fundr'),
  path('userlocation/', views.store_user_location, name='store_user_location'),
]