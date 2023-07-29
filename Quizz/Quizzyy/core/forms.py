from django.forms import ModelForm
from .models import *

# FORM
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model= User
        fields = ['username', 'email', 'password1', 'password2']
        
        
class CategoryForm(ModelForm):
    
    class Meta:
        model = Category
        fields = "__all__"


        
class QuizzAddForm(ModelForm):
    class Meta:
        model = QuizzAdd
        fields = "__all__"