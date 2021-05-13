from django.contrib import admin
from django.urls import path,include
from API import views 

urlpatterns = [
    path('user/<str:phonenumber>',views.home_user),
    path('user/<str:phonenumber>/<str:devicename>',views.home_user),
]