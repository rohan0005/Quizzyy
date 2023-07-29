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
    

   
@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
#@admin_only
def addQuizz(request):
    quizzAddForm = QuizzAddForm()
    categoryForm = CategoryForm()
    
    if request.method == "POST":
        if "addQuizz" in request.POST:
            quizzAddForm = QuizzAddForm(request.POST)
            if quizzAddForm.is_valid():
                categoryObj = quizzAddForm.cleaned_data.get('category')
                categoryName = categoryObj.category
                quizzAddForm.save()
                messages.success(request, "Successfully added quizz for category - " + categoryName)
            return redirect(request.path)
            
        
        # elif "quizz" in request.POST:
        else:
            categoryForm = CategoryForm(request.POST)
            if categoryForm.is_valid():
                categoryName = categoryForm.cleaned_data.get('category')
                categoryForm.save()
                messages.success(request, "Successfully added category - " + categoryName)
            return redirect(request.path)
    
    
        
        
    context = {
        'form': quizzAddForm,
        'categoryForm': categoryForm,
        
    }
    
    return render(request, 'addQuizz.html', context)
    
    
    
    
# Showing available quizes for selected category
    
def SelectedCategory(request):
    return render (request, 'SelectedCategory.html')
        
    
    
    
def quizzCategories(request):
    
    categoryDetails = Category.objects.all()

    context = {
        'categoryDetails': categoryDetails
    }

    
    
    return render (request, 'quizzCategories.html', context)
 