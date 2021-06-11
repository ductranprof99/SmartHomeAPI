from django.urls import path
from . import views

urlpatterns = [
    path('statistics?device-type=light&range=week',views.StatisticManager.as_view()),
]