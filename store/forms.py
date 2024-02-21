from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from dataclasses import fields
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User



class CustomUserCreationForm(UserCreationForm):
    pass

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
