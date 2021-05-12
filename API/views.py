from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import json
from API.models import *
from API.serializers import *
from rest_framework.decorators import api_view
from SmartHomeAPI import connect



@api_view(['GET','POST'])
def home_user(request,homename:str):
    if request.method == 'GET':
        homes = Home.objects.all()
        homes = homes.filter(house_name=homename)
        home_data = HomeUserSerializer(homes, many=True).data
        #a = home_data[0]
        #print(a)
        if (home_data != {} and home_data != None):
            print(Home.objects.all())
            return JsonResponse(home_data, safe=False,  status=status.HTTP_202_ACCEPTED)
        return JsonResponse(None, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def home_admin(request,homename:str):
    if request.method == 'POST':
        home_need_update = Home.objects.get(house_name=homename)

        data = json.loads(request.body)
        """
        if data.change_device != null -> update device
        if data.change_schedule != null -> update schedule
        """
        # home = Home()
        # devicee = {'device_name':'abba','description':'asfasdf','current_status':True,'automation_status':'asfas','mode':1,'schedule':None}
        # home.devices = [devicee,devicee]
        # home.house_name = 'asdfasf'
        # home.address = 'asdfasf'
        # home.save()




# @api_view(['GET','POST','DELETE'])
# def devicesAdmin(request,deviceid):
#     if request.method =='GET':
#         data = json.loads(request.body)
#     if request.method == 'POST':
#         data_serialized = DevicesAdminSerializer(data = request.data)
#         # if iscreate = true
#         # then create unique device name
#         # then create
#         # if 
#         if data_serialized.is_valid():
#             response = data_serialized.save()
#             alldevice = DevicesAdmin.objects.all()
#             homes = homes.filter(house_name=)
#             home_data = HomeSerializer(homes, many=True).data
#             return JsonResponse({'new_device_id':}, status=status.HTTP_201_CREATED)
#     if request.method == 'DELETE':
#         pass