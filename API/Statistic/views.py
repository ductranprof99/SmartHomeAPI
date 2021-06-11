from django.http.response import JsonResponse
from rest_framework import status
from API.models import *
from API.serializers import *
from ..views import SmartHomeAuthView
from bson.json_util import ObjectId
from .. import analizer


class StatisticManager(SmartHomeAuthView):
    abstract = analizer.Statistic()

    def get(self):
        claimedPhoneNumber = self.request.user.phone_number
        try:
            Home.objects.get(phone_number=claimedPhoneNumber)
        except:
            return self.responseUnauthed(claimedPhoneNumber)

    
