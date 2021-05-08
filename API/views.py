from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from API.models import *
# from API.serializers import *
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET','POST','DELETE'])
def device(request, houseid:int, deviceid:int):
    #double request
    if request.method == 'GET':
        #result = Device.objects.all()
        mortal = None
        for device in JsonDetailDevice["devices"]:
           if(device["device-id"]==deviceid):
               mortal = device
        result = ({
            "device": mortal,
            "length": 1
        })
        return JsonResponse(mortal, status=status.HTTP_200_OK)
    pass
    


@api_view(['GET'])
def devices(request, houseid:int):
    if request.method == 'GET':
        return JsonResponse(returnJson, status=status.HTTP_200_OK)
    

returnJson = ({
            "devices": [
                {"device-id": 123,"kind": "Light", "device-name": "Cac"},
                {"device-id": 124,"kind": "Fan", "device-name": "Quat tran"}
            ],
            "length": 2
        })

JsonDetailDevice = ({
            "devices": [
                {
                    "device-id": 123,
                    "kind": "Light", 
                    "device-name": "Den nha tam",
                    "mode":"scheduler", 
                    "scheduler":[
                        {
                            "sche-id": 123,
                            "time-on": "12:00",
                            "time-off": "18:00",
                            "loop": True,
                            "sche-day": {
                                "2": True,
                                "3": False
                            }
                        }
                    ],
                },
                {"device-id": 124,"kind": "Fan", "device-name": "Quat tran"}
            ],
            "length": 2
        })