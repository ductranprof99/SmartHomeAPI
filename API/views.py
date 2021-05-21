from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import status
import json
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


@api_view(['GET','POST'])
def allusers(request):
    homes = Home.objects.all()
    result = {'users': []}
    home_data = HomeSerializer(homes, many=True).data
    for home in home_data:
        home = dict(home)
        bla = {}
        bla['phone_number'] = home['phone_number']
        bla['address'] = home['address']
        result['users'] += [bla]
    # print(result)
    return JsonResponse(result, safe=False,  status=status.HTTP_202_ACCEPTED)

@api_view(['GET','POST'])
def home_user(request,phonenumber:str,devicename = ''):
    if request.method == 'GET':
        """
        need to fix the for loop later, this prototype get data directly from adafruit, but
        we want to get data from the database (the message function in mqtt is not done yet)
        """
        homes = Home.objects.all()
        homes = homes.filter(phone_number=phonenumber)
        home_data = HomeSerializer(homes, many=True).data
        home_data[0]['devices'] = json.loads(home_data[0]['devices'])
        if devicename == '':
            res = {}
            res["home_id"] = home_data[0]['phone_number']
            res['devices'] = []
            count = 1
            for d in home_data[0]['devices']:
                current_device = {}
                current_device['device-id'] = count  # fix here 2, i want to store this in database, lesswork and more safe, but naming stage kinda sus
                complete_feedid = phonenumber+ '-' + str(count)
                current_device['device_name'] = d['device_name']
                current_device['description'] = d['description']
                current_device['status'] = mqtt.access.getFeedOneData(complete_feedid).value  #fix here with that naming below
                current_device['device_type'] = d['device_type']
                if d['device_type'] == "temperature" or d['device_type'] == "humid":
                    current_device['unit'] = d['unit']
                count+=1
                res['devices'] += [current_device]
            return JsonResponse(res, safe=False,  status=status.HTTP_202_ACCEPTED)
            ## still not done with the device delete, im done with my life
        elif devicename != '':
            paralelcheck = {'1': 'Sun','2': 'Mon','3': 'Tue','4': 'Wed','5': 'Thu','6': 'Fri','1': 'Sat'}
            device_order = int(devicename)
            result = {"device-id": devicename}
            result.update(home_data[0]['devices'][device_order-1])
            result['schedule'] = json.loads(result['schedule'])
            for d in result['schedule']:
                d["is_repeat"] = bool(d["is_repeat"])
                if d['is_repeat'] == 'True':
                    res_repeat = {}
                    for key in paralelcheck:
                        if key in d['repeat_day']:
                            res_repeat[paralelcheck[key]] = True
                        else:
                            res_repeat[paralelcheck[key]] = False
                    d['repeat_day'] = res_repeat
                    print(d['repeat_day'])
            return JsonResponse(result, safe=False,  status=status.HTTP_202_ACCEPTED)
        return JsonResponse(None, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        print(request.data)
        device_id = request.data["device_id"]
        data = request.data["data"]
        res = {"device_id":device_id,"data":data}
        complete_feedid = phonenumber+'-' + str(device_id)
        print(complete_feedid)
        print(mqtt.access.sendDataToFeed(complete_feedid,str(data)))
        return JsonResponse(res, safe=False,  status=status.HTTP_202_ACCEPTED)
        #mqtt.access.sendDataToFeed()
        # home = Home()
        # schedule = Schedule()
        # schedule.time_on = '10:00'
        # schedule.time_off = '18:00'
        # schedule.is_repeat = True
        # schedule.repeat_day = '[1,2,3]'
        # device1 = Device()
        # device1.device_name = 'den nha tam'
        # device1.description = 'o trong can nha hoang'
        # device1.feed_name = 'abba'
        # device1.device_type = 'light'
        # device1.current_status = True
        # device1.value = '1'
        # device1.mode = 1
        # device1.schedule = [model_to_dict(schedule)]
        # home.devices = [model_to_dict(device1)]
        # home.home_name = 'My house'
        # home.address = 'Dong Hoa, Di An'
        # home.save()
        # return JsonResponse({'a':'a'}, safe=False,  status=status.HTTP_201_CREATED)


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
                return Response(data, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'phone number or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)




