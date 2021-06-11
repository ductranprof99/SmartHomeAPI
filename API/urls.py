from django.urls import path, include
from API import views 
from .User import urls as userURLs
from .Device import urls as deviceURLs
from .Schedule import urls as schedURLs
from .Statistic import urls as statisticsURLs

urlpatterns = [
    path('users',views.allusers),
    path('profile',views.HomeInfo.as_view()),
    path('addhome',views.addHome),
    path('', include(userURLs)),
    path('', include(deviceURLs)),
    path('', include(schedURLs)),
    path('', include(statisticsURLs)),
]