from django.urls import path, include
from API import views 
from .User import urls as userURLs

urlpatterns = [
    path('users',views.allusers),
    path('@<str:phonenumber>/devices',views.DeviceList.as_view()),
    path('@<str:phonenumber>/devices/<str:device_id>',views.DeviceInfo.as_view()),
    path('profile',views.HomeInfo.as_view()),
    path('adddevice',views.addDevice),
    path('addhome',views.addHome),
    path('addsched',views.ModifySchedule.as_view()),
    path('', include(userURLs))
]