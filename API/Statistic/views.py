from django.http.response import JsonResponse
from rest_framework import status
from API.models import *
from API.serializers import *
from ..views import SmartHomeAuthView
from bson.json_util import ObjectId


class StatisticManager(SmartHomeAuthView):
    pass
