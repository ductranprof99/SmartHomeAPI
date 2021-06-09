from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('loginStatus', views.TestAuth.as_view(), name='loginStatus'),
    path('change-password', views.ChangePassword.as_view(), name='change-password'),
]