from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from API.models import *
from API.serializers import *
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def schelude(request, houseid:int, deviceid:int):
    pass


