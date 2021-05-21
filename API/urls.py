from django.contrib import admin
from django.urls import path,include
from API import views 
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('users',views.allusers),
    path('@<str:phonenumber>/devices',views.home_user),
    path('@<str:phonenumber>/devices/<str:devicename>',views.home_user),
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('login', views.UserLoginView.as_view(), name='login'),
]