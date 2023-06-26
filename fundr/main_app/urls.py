from django.urls import path
from . import views

urlpatterns = [
  path('', views.login, name='login'),
  path('home', views.home, name='home'),
  path('explore/', views.explore, name='explore'),
  path('following/', views.following, name='following'),
  path('about/', views.about, name='about'),
  path('contact/', views.contact, name='contact'),
  path('terms/', views.terms, name='terms'),
  path('settings/', views.SettingsView.as_view(), name='settings'),
  path('fundrs/<int:fundr_id>', views.fundrs_detail, name='detail'),
  path('fundrs/<int:fundr_id>/add_post/', views.add_post, name='add_post'),
  path('accounts/signup/', views.signup, name='signup'),
  path('your_fundrs/', views.your_fundrs, name='your_fundrs'),
  path('your_fundrs/new_fundr', views.FundrCreate.as_view(), name='new_fundr'),
  path('fundrs/<int:pk>/update', views.FundrUpdate.as_view(), name='update_fundr'),
  path('fundrs/<int:pk>/delete', views.FundrDelete.as_view(), name='delete_fundr'),
  path('userlocation/', views.store_user_location, name='store_user_location'),
  path('fundrs/<int:fundr_id>/posts/<int:post_id>', views.delete_post, name='delete_post'),
  path('settings/update/<int:pk>', views.SettingsUpdate.as_view(), name='update_settings'),
]
