from django.forms import ModelForm
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
        fields = ('name', 'bio', 'description', 'goal', 'location')


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'content')
