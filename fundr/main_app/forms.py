from django.forms import ModelForm
from django import forms
from .models import User, Profile, Fundraiser, Post

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'location')
    
    
class FundrForm(ModelForm):
    class Meta:
        model = Fundraiser
        fields = ('name', 'bio', 'description', 'goal', 'location', 'image')


class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 35, 'class': 'align-self-start form-label'}))
    image = forms.ImageField(required=False)
    owner = forms.IntegerField(required=True, widget=forms.HiddenInput())
    fundraiser = forms.IntegerField(required=True, widget=forms.HiddenInput())


class SettingsForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['catchment', 'avatar']
