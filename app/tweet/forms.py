from django import forms
from .models import Tweet, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
  email = forms.EmailField()
  first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  profileimg = forms.ImageField(required=False)
  
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profileimg')


class TweetForm(forms.ModelForm):
  class Meta:
    model = Tweet
    fields = ['text', 'photo']

class ProfileEditForm(forms.ModelForm):
  first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

  class Meta:
    model = Profile
    fields = ['profileimg', 'coverimg', 'bio', 'location']