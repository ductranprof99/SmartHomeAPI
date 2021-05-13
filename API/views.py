from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.parsers import JSONParser 
from rest_framework import status
import json

from rest_framework.serializers import Serializer
from API.models import *
from API.serializers import *
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from SmartHomeAPI import settings


@api_view(['GET','POST'])
def home_user(request,phonenumber:str,devicename = ''):
    if request.method == 'GET':
    
        homes = Home.objects.all()
        homes = homes.filter(phone_number=phonenumber)
        home_data = HomeSerializer(homes, many=True).data
        home_data[0]['devices'] = json.loads(home_data[0]['devices'])
        if devicename == '':
            res = {}
            res["home_id"] = home_data[0]['_id']
            res['devices'] = []
            count = 1
            for d in home_data[0]['devices']:
                current_device = {}
                current_device['device-id'] = count
                current_device['device_name'] = d['device_name']
                current_device['description'] = d['description']
                current_device['status'] = d['current_status']
                current_device['device_type'] = d['device_type']
                count+=1
                res['devices'] += [current_device]
            return JsonResponse(res, safe=False,  status=status.HTTP_202_ACCEPTED)
        elif devicename != '':
            device_order = int(devicename)
            result = {"device-id": devicename}
            result.update(home_data[0]['devices'][device_order-1])
            result['schedule'] = json.loads(result['schedule'])
            for d in result['schedule']:
                if d['is_repeat'] == 'True':
                    res_repeat = {}
                    if '1' in d['repeat_day']:
                        res_repeat['Sun'] = 1
                    else: res_repeat['Sun'] = 0
                    if '2' in d['repeat_day']: 
                        res_repeat['Mon'] = 1
                    else: res_repeat['Mon'] = 0   
                    if '3' in d['repeat_day']:
                        res_repeat['Tue'] = 1 
                    else: res_repeat['Tue'] = 0
                    if '4' in d['repeat_day']:
                        res_repeat['Wed'] = 1 
                    else: res_repeat['Wed'] = 0
                    if '5' in d['repeat_day']:
                        res_repeat['Thu'] = 1 
                    else: res_repeat['Thu'] = 0
                    if '6' in d['repeat_day']:
                        res_repeat['Fri'] = 1 
                    else: res_repeat['Fri'] = 0
                    if '5' in d['repeat_day']:
                        res_repeat['Sat'] = 1 
                    else: res_repeat['Sat'] = 0
                    d['repeat_day'] = res_repeat
                    print(d['repeat_day'])
            return JsonResponse(result, safe=False,  status=status.HTTP_202_ACCEPTED)
        return JsonResponse(None, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        pass
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







# @api_view(['GET','POST','DELETE'])
# def home_admin(request,homeid:str):
#     if request.method == 'GET':
#         homes = Home.objects.all()
#         homes = homes.filter(_id=homeid)
#         home_data = HomeSerializer(homes, many=True).data
#         if (home_data != {} and home_data != None):
#             print(home_data['devices'])
#         return JsonResponse(home_data, safe=False,  status=status.HTTP_202_ACCEPTED)
#         #return JsonResponse(None, status=status.HTTP_400_BAD_REQUEST)
#     if request.method == 'POST':
#         home_need_update = Home.objects.get(_id=homeid)
#         data = json.loads(request.body)
#         pass
#     if request.method == 'DELETE':
#         pass


# @api_view(['GET','POST','DELETE'])
# def device_admin(request,deviceid = None):
#     if request.method == 'GET':
#         alldevice = DevicesAdmin.objects.all()
#         devices_home = alldevice.filter(_id = deviceid)
#         admin_device = DevicesAdminSerializer(devices_home,many=True).data
#         homes = Home.objects.all()
#         homes = homes.filter(_id=admin_device['home_id'])
#         device_home_data = HomeSerializer(homes, many=True).data['devices']
#         if (admin_device != None and device_home_data != None):
#             return JsonResponse([device_home_data,admin_device], safe=False,  status=status.HTTP_202_ACCEPTED)
#         return JsonResponse(None, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'POST':
#         pass
#     if request.method == 'DELETE':
#         pass
        
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
# def homeAdmin(request,homeid:str):
#     if request.method =='GET':
#         allhome = Home.objects.all()
#         if homeid != None:
#             home = None
#             home = allhome.filter(_id=homeid)
#             home_data = HomeSerializer(home, many=True).data
#             return JsonResponse(home_data, status=status.HTTP_202_ACCEPTED)
#         home_data = HomeSerializer(allhome, many=True).data
#         if home_data != None:
#             return JsonResponse(home_data, status=status.HTTP_202_ACCEPTED)
#         return JsonResponse(None, status=status.HTTP_400_BAD_REQUEST)
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         data_serialized = DevicesAdminSerializer(data = request.data)
#         if iscreate = true
#         then create unique device name
#         then create
#         if 
#         if data_serialized.is_valid():
#             response = data_serialized.save()
#             alldevice = DevicesAdmin.objects.all()
#             homes = homes.filter(home_name=)
#             home_data = HomeSerializer(homes, many=True).data
#             return JsonResponse({'new_device_id':}, status=status.HTTP_201_CREATED)
#     if request.method == 'DELETE':
#         pass