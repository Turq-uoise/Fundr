from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
import datetime

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=200)
    location = models.CharField(max_length=7, default="")
    latitude = models.FloatField(default=0.0, null=True)
    longitude = models.FloatField(default=0.0, null=True)
    catchment = models.FloatField(default=100)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


    

class Fundraiser(models.Model):
    name = models.CharField(max_length = 100)
    bio  = models.CharField(max_length = 280)
    description = models.CharField(max_length = 1000)
    image = models.CharField(max_length=200, default="https://fundr.fly.dev/static/main_app/home_pic.png", null=True, blank=True)
    goal = models.FloatField(
        default=1000.0,
        validators=[
            MaxValueValidator(100000,0),
            MinValueValidator(10.0)
            ]
        )
    current = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0)
        ]
        )
    location = models.CharField(max_length=7,)
    lat = models.FloatField(default=0.0)
    long = models.FloatField(default=0.0)
    distance_from_user = models.FloatField(default=0.0)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE) 
    followers = models.ManyToManyField(User)
    # deletes all fundraisers when owners account is deleted // poses some opportunities for would-be scammers -- future implementation should have an archive database that holds details of fundraisers and their owners (beyond scope given timeframe)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
      return reverse('detail', kwargs={'fundr_id': self.id})
    

class Post(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    fundraiser = models.ForeignKey(Fundraiser, on_delete=models.CASCADE)
    image = models.CharField(max_length=200, default="http://localhost:8000/static/main_app/home_pic.png")
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)
    date_created = models.DateField(_("Date"), default=datetime.date.today)

    def __str__(self):
        return self.content
    
    
    



