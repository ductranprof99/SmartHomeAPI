from django.urls import path
from . import views

urlpatterns = [
    path('@<str:phonenumber>/devices',views.DeviceList.as_view()),
    path('@<str:phonenumber>/devices/<str:device_id>',views.DeviceInfo.as_view()),
    path('adddevice',views.addDevice),
]