from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# for storing user in a student group 
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from . decorators import *


# Create your views here.

def index(request):
    return render(request, 'index.html',)


@unauthenticated_user
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
            
            
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'login.html')



def logoutUser(request):
    logout(request)
    return redirect('login')






@unauthenticated_user
def register(request):
    
    form = CreateUserForm()
        
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
                
            group = Group.objects.get(name='student')
            user.groups.add(group)
                
            messages.success(request,"Account Created for " + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)
    

   
   
def addQuizz(request):
    return render(request, 'addQuizz.html')
    
    
    
    
# Showing available quizes for selected category
    
def SelectedCategory(request):
    return render (request, 'SelectedCategory.html')
        
    
    