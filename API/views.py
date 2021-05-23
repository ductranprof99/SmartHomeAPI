from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import status
import json
from bson.json_util import ObjectId

from API.models import *
from API.serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from SmartHomeAPI import settings
from . import mqtt
import ast
import API.stringProcess

@api_view(['GET','POST'])
def allusers(request):
    homes = Home.objects.all()
    result = {'users': []}
    home_data = AllHomeSerializer(homes, many=True).data
    for home in home_data:
        home = dict(home)
        result['users'] += [home]
    # print(result)
    return JsonResponse(result, safe=False,  status=status.HTTP_202_ACCEPTED)

@api_view(['GET','POST'])
def home_user(request,phonenumber:str,devicename = ''):
    homes = Home.objects.all()
    devices_all = Device.objects.all()
    homes = homes.filter(phone_number=phonenumber)
    home_data = HomeSerializer(homes, many=True).data
    home_devices = json.loads(home_data[0]['devices'])
    if request.method == 'GET':
        """
        need to fix the for loop later, this prototype get data directly from adafruit, but
        we want to get data from the database (the message function in mqtt is not done yet)
        """
        if devicename == '':
            res = {}
            res["home_id"] = home_data[0]['phone_number']
            devices = devices_all.filter(home_phonenumber=phonenumber)
            device_ord = DeviceOnHomeSerializer(devices, many=True).data
            res['devices'] = []
            count = 1
            for d in device_ord:
                current_device = dict(d)
                current_device['device_id'] = count
                count += 1
                res['devices'] += [current_device]
            return JsonResponse(res, safe=False,  status=status.HTTP_202_ACCEPTED)
        else:
            devices = devices_all.filter(device_id=home_devices[int(devicename)-1])
            device_ord = DeviceDetailSerializer(devices, many=True).data
            result = {'device_id':int(devicename)-1}
            result.update(dict(device_ord))
            return JsonResponse(result, safe=False,  status=status.HTTP_202_ACCEPTED)
    if request.method == 'POST':
        pass
    return JsonResponse({}, safe=False,  status=status.HTTP_202_ACCEPTED)



class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()

            return JsonResponse({
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({
                'error_message': 'This phone number has already exist!',
                'errors_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['phone_number'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                    'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                    'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
                }
                # save into database

                #
                return Response(data, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'phone number or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','POST'])
def addData(request):

    """
    require admin user, i will make  IsAuthencation(request.data[token] in here)
    """
    if request.method == 'POST':
        device = Device()
        device._id = ObjectId()
        device.device_id = str(device._id)
        device.description= request.data['']
        device.device_name = request.data['']
        device.schedule = []
        device.device_type = request.data['']
        device.current_status = request.data['']
        device.unit = request.data['']
        device.mode = request.data['']
        device.home_phonenumber = request.data['']
        device.feed_name = str(device._id) + device.home_phonenumber
        device.save()
        print(device)
        return  JsonResponse({'a':'a'}, safe=False,  status=status.HTTP_202_ACCEPTED)

@api_view(['GET','POST'])
def addHome(request):

    """
    require admin user, i will make  IsAuthencation(request.data[token] in here)
    """
    if request.method == 'POST':
        device = Device()
        device._id = ObjectId()
        device.device_id = str(device._id)
        device.description= request.data['']
        device.device_name = request.data['']
        device.schedule = []
        device.device_type = request.data['']
        device.current_status = request.data['']
        device.unit = request.data['']
        device.mode = request.data['']
        device.home_phonenumber = request.data['']
        device.feed_name = str(device._id) + device.home_phonenumber
        device.save()
        print(device)
        return  JsonResponse({'a':'a'}, safe=False,  status=status.HTTP_202_ACCEPTED)