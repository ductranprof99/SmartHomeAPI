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
def home_user(request,phonenumber:str,deviceOrder = None):
    homes = Home.objects.all()
    devices = Device.objects.all()
    schedules = Schedule.objects.all()
    homes = homes.filter(phone_number=phonenumber)
    home_data = HomeSerializer(homes, many=True).data
    home_devices = json.loads(home_data[0]['devices'])
    command = {'ON':'1','OFF':'2'}
    devices_led = devices.filter(phone_number=phonenumber)
    data_form = {'id':'','name':'','data':'','unit':''}
    if request.method == 'GET':
        if deviceOrder == None:
            res = {"home_id":home_data[0]['phone_number'],'devices':[]}
            device_ord = DeviceOnHomeSerializer(devices_led, many=True).data
            for d in device_ord:
                a = {'device_id':device_ord.index(d)}
                a.update(dict(d))
                res['devices'] += [a]
            return JsonResponse(res, safe=False,  status=status.HTTP_202_ACCEPTED)
        else:
            device_ord = dict(DeviceDetailSerializer(devices_led,many=True).data[deviceOrder-1])
            order = device_ord.pop('device_id')
            schedules = schedules.filter(device_id=order)
            schedule_ord = ScheduleSerializer(schedules,many=True).data
            result = {'device_id':deviceOrder}
            result['schedules'] = [dict(sched) for sched in schedule_ord]
            result.update(device_ord)
            return JsonResponse(result, safe=False,  status=status.HTTP_202_ACCEPTED)
    if request.method == 'POST':
        if deviceOrder == None:
            income = request.data
            device_id_int  = int(income['device_id'])-1
            real_devi_id = home_devices[deviceOrder-1]['device_id']
            device = devices.filter(device_id=real_devi_id)
            device_ord = dict(DeviceDetailSerializer(device).data)
            data_form['unit'] = device_ord['unit']
            data_form['id'] = device_ord['feed_name']
            data_form['data'] = command[income['data']]
            data_form['name'] = device_ord['device_type']
            mqtt.access.sendDataToFeed(device_ord['feed_name'],data_form)
        else :
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
def addDevice(request):
    """
    demo : i will make  IsAuthencation(request.data[token] in here) in every views funciton
    this thing for test add data
    """
    if request.method == 'POST':
        device = Device()
        device._id = ObjectId()
        device.device_id = str(device._id)
        device.phone_number = request.data['phone_number']
        device.description= request.data['description']
        device.device_name = request.data['device_name']
        device.device_type = request.data['device_type']
        device.status = request.data['status']
        device.unit = request.data['unit']
        device.automation_mode = request.data['automation_mode']
        device.schedules = request.data['schedules']
        device.feed_name = request.data['feed_name']
        device.save()
        print(device)
        return  JsonResponse({'a':'a'}, safe=False,  status=status.HTTP_202_ACCEPTED)

@api_view(['GET','POST'])
def addHome(request):
    """
    this thing for test add data
    """
    if request.method == 'POST':
        home = Home()
        home.address= request.data['address']
        home.home_name = request.data['home_name']
        home.devices = []
        home.phone_number = request.data['phone_number']
        home.save()
        print(home)
        return  JsonResponse({'a':'a'}, safe=False,  status=status.HTTP_202_ACCEPTED)

