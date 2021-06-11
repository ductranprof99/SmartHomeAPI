from django.urls import path
from . import views

urlpatterns = [
    path('statistic',views.StatisticManager.as_view()),
]