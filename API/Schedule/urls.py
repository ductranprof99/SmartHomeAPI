from django.urls import path
from . import views

urlpatterns = [
    path('addsched',views.ModifySchedule.as_view()),
]