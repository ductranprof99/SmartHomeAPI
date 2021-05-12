from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import json
from API.models import *
from API.serializers import *
from rest_framework.decorators import api_view




@api_view(['GET','POST'])
def home_user(request,homename:str):
    if request.method == 'GET':
        homes = Home.objects.all()
        homes = homes.filter(home_name=homename)
        home_data = HomeUserSerializer(homes, many=True).data
        if (home_data != {} and home_data != None):
            print(Home.objects.all())
            return JsonResponse(home_data, safe=False,  status=status.HTTP_202_ACCEPTED)
        return JsonResponse(None, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST','DELETE'])
def device_admin(request,homeid:str):
    if request.method == 'GET':
        alldevice = DevicesAdmin.objects.all()
        devices_home = alldevice.filter(home_id=homeid)
        admin_device = DevicesAdminSerializer(devices_home,many=True)
        homes = Home.objects.all()
        homes = homes.filter(id=homeid)
        device_home_data = HomeUserSerializer(homes, many=True).data
        if ([admin_device,device_home_data] != [{},{}]):
            print(Home.objects.all())
            return JsonResponse([device_home_data['devices'],admin_device], safe=False,  status=status.HTTP_202_ACCEPTED)
        return JsonResponse(None, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        pass
    # if request.method == 'POST':
    #     home_need_update = Home.objects.get(home_name=homename)
    #     data = json.loads(request.body)
        
    #     """
    #     if data.change_device != null -> update device
    #     if data.change_schedule != null -> update schedule
    #     """
        # home = Home()
        # devicee = {'device_name':'abba','description':'asfasdf','current_status':True,'automation_status':'asfas','mode':1,'schedule':None}
        # home.devices = [devicee,devicee]
        # home.home_name = 'asdfasf'
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
#             homes = homes.filter(home_name=)
#             home_data = HomeSerializer(homes, many=True).data
#             return JsonResponse({'new_device_id':}, status=status.HTTP_201_CREATED)
#     if request.method == 'DELETE':
#         pass