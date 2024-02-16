from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from dataclasses import fields
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',"first_name","last_name","email","password1","password2"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
