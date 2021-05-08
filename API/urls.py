from django.contrib import admin
from django.urls import path,include
from API import views 

urlpatterns = [
    path('@<str:houseid>/devices', views.devices),
    path('@<str:houseid>', views.house),
    path('house/<int:houseid>/device/<int:deviceid>', views.device),
]