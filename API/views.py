from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from API.models import *
from API.serializers import *
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET','PUT','DELETE'])
def house(request, houseid:str):
    if request.method == 'GET':
        pass

@api_view(['GET','POST','DELETE'])
def device(request, houseid, deviceid:int):
    #double request
    if (isinstance(houseid,int)):
        pass
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

@api_view(['GET'])
def house(request,houseid):
    if request.method == 'GET':
        house_data =  demohouse #JSONParser().parse(demohouse)
        house_serializer = HouseSerializer(data=user_data)
        if house_serializer.is_valid():
            house_serializer.save()
            return JsonResponse(house_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(house_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


demohouse = ({
    "phoneNumber": "011234vsdf134",
    "name": "asdfasasdfdf",
    "password": "adsfasdf",
    "address": "asfdasdfafs"
})