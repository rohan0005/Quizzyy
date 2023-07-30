from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name= "home"),
    path('login/', views.loginPage, name= "login"),
    path('logout/', views.logoutUser, name= "logout"),


    path('registerr/', views.registerr, name='register'),
    
    path('SelectedCategory/', views.SelectedCategory, name='SelectedCategory'),
    
    
    path('addQuizz/', views.addQuizz, name='addQuizz'),
    
    path('quizzCategories/', views.quizzCategories, name='quizzCategories'),
    
    path('startQuizz/<str:category_name>/', views.startQuizz, name='startQuizz'),
    
    path('viewResult/', views.viewResult, name='viewResult'),
    
    
    
    
    
    
]