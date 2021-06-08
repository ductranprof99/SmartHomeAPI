from django.urls import path, include
from API import views 
from .User import urls as userURLs

urlpatterns = [
    path('users',views.allusers),
    path('@<str:phonenumber>/devices',views.home_user),
    path('@<str:phonenumber>/devices/<int:deviceOrder>',views.home_user),
    path('adddevice',views.addDevice),
    path('addhome',views.addHome),
    path('addsched',views.addSchedule),
    path('', include(userURLs))
]