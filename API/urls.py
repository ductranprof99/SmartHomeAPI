from django.contrib import admin
from django.urls import path,include
from API import views 

urlpatterns = [
    path('house/<int:houseid>/devices', views.devices), #all devices info...
    path('house/<int:houseid>/device/<int:deviceid>', views.device),
]