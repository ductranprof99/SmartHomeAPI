from django.contrib import admin
from django.urls import path,include
from API import views 

urlpatterns = [
    path('user/<str:homename>',views.home_user)
]