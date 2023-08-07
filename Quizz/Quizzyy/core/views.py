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
    
    if 'name' in request.COOKIES and request.COOKIES['name']:
        cookieData = request.COOKIES['name']
        return render(request, 'index.html', {'cookieData' : cookieData})
    else:
        return render(request, 'index.html')



@unauthenticated_user
def loginPage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
            
            
        if user is not None:
            login(request, user)
             
            response = redirect('home')
    
            response.set_cookie('name', username) # max_age=60
            
            return response
    
             
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'login.html')







def logoutUser(request):

    response = redirect('login')
    
    response.delete_cookie('name')
    
    logout(request)
    
    return response








@unauthenticated_user
def registerr(request):
    
    form = CreateUserForm()
        
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            user = form.save()
            username = form.cleaned_data.get('username')
            selectedGroup = form.cleaned_data.get('status')
            
            #print("Selected group is", selectedGroup)
            
            if selectedGroup:
                #print("Selected group is", selectedGroup)
                group = Group.objects.get(name=selectedGroup)
                
                user.groups.add(group)
                
                messages.success(request,"Account Created for " + username)
                return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)
    





def teacherRegister(request):
    return render (request, 'teacherRegister.html')






   
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
    

    
    
    
def quizzCategories(request):
    
    categoryDetails = Category.objects.all()

    context = {
        'categoryDetails': categoryDetails
    }

    
    
    return render (request, 'quizzCategories.html', context)
 
 
 
@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])    
def startQuizz(request, category_name):
    
    
    cats = QuizzAdd.objects.filter(category__category=category_name)
    
    
    if request.method == "POST":
        
        cat = cats.first()
        if cat:
            
            # store user answers in dictionary 
            user_answers={}
            # # retrieve all the quiz questions associated with a specific category.
            category = Category.objects.get(category=category_name)
            quizzes = QuizzAdd.objects.filter(category=category)
            totalQuestions = quizzes.count()
            
            totalCorrectAns = 0
            
            for quizz in quizzes:
                
                user_answer = request.POST.get(str(quizz.id))
                user_answers[quizz.id] = user_answer
          
                if user_answer == quizz.correctAnswer:
                    totalCorrectAns += 1
                    
                    
            context ={
                'quizzes': quizzes,
                'totalQuestions': totalQuestions,
                'totalCorrectAns': totalCorrectAns,
                'user_answers' : user_answers,
            }
            
            
        else:
            print("No category found in the queryset.")
        
        return render(request, 'viewResult.html',context)
        
    
    context ={
        'cats': cats
    }
    
    return render (request, 'startQuizz.html', context)
     
from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

     
@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])       
def viewResult(request):
    return render(request, 'viewResult.html')