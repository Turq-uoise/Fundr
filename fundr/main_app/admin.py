from django.contrib import admin
from .models import Fundraiser, Post, Profile

# Register your models here.
admin.site.register(Fundraiser)
admin.site.register(Post)
admin.site.register(Profile)