from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.parsers import JSONParser 
from rest_framework import status
import json
from API.models import *
from API.serializers import *
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict

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