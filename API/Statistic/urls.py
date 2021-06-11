from django.urls import path
from . import views

urlpatterns = [
    path('statistics',views.StatisticManager.as_view()),
]