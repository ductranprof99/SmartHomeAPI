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
from ast import literal_eval
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
    devices = Device.objects.all()
    schedules = Schedule.objects.all()
    homes = homes.filter(phone_number=phonenumber)
    home_data = HomeSerializer(homes, many=True).data
    home_devices = json.loads(home_data[0]['devices'])
    if request.method == 'GET':
        if devicename == '':
            res = {}
            res["home_id"] = home_data[0]['phone_number']
            devices = devices.filter(home_phonenumber=phonenumber)
            device_ord = DeviceOnHomeSerializer(devices, many=True).data
            res['devices'] = [{'device_id':device_ord.index(d)}.update(dict(d)) for d in device_ord]
            return JsonResponse(res, safe=False,  status=status.HTTP_202_ACCEPTED)
        else:
            real_devi_id = home_devices[int(devicename)-1]['device_id']
            device = devices.filter(device_id=real_devi_id)
            device_ord = dict(DeviceDetailSerializer(device).data)
            schedules = schedules.filter(device_id=real_devi_id)
            schedule_ord = ScheduleSerializer(schedules,many=True).data
            result = {'device_id':int(devicename)-1}
            result['schedules'] = [dict(sched) for sched in schedule_ord]
            result.update(device_ord)
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
        device.description= request.data['description']
        device.device_name = request.data['device_name']
        device.schedule = []
        device.device_type = request.data['device_type']
        device.status = request.data['status']
        device.unit = request.data['unit']
        device.automation_mode = request.data['automation_mode']
        device.phone_number = request.data['phone_number']
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
        home = Home()
        home.address= request.data['address']
        home.device_name = request.data['']
        home.device_type = request.data['']
        home.devices = []
        home.phone_number = request.data['phone_number']
        home.save()
        print(home)
        return  JsonResponse({'a':'a'}, safe=False,  status=status.HTTP_202_ACCEPTED)