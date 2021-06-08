from django.urls import path, include
from API import views 
from .User import urls as userURLs

urlpatterns = [
    path('users',views.allusers),
    path('@<str:phonenumber>/devices',views.DeviceList.as_view()),
    path('@<str:phonenumber>/devices/<int:deviceOrder>',views.DeviceList.as_view()),
    path('adddevice',views.addDevice),
    path('addhome',views.addHome),
    path('addsched',views.addSchedule),
    path('', include(userURLs))
]