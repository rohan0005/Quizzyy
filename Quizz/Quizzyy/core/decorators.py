from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
         if request.user.is_authenticated:
            return redirect('home')
    
         else:
             
            #  IF not auth then do this
            return view_func(request, *args, **kwargs)
             
    return wrapper_func



def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                home_page_url = reverse('home')
                message = f"<p>You are not authorized. Go back to <a href='{home_page_url}'>Home Page</a> </p>"
                return HttpResponse(message)
                
            
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'student':
            return redirect('home')
        if group == 'teacher':
            return view_func(request, *args, **kwargs)
    return wrapper_function
    