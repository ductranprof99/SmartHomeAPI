from django.http.response import JsonResponse
from rest_framework import status
from API.models import *
from API.serializers import *
from ..views import SmartHomeAuthView
from bson.json_util import ObjectId
import json
from ..mongo import db
from .. import Adafruit
from ast import literal_eval
from rest_framework.decorators import api_view

class DeviceList(SmartHomeAuthView):
    
    def get(self, request, phonenumber: str):
        if self.request.user.phone_number != phonenumber:
            return self.responseUnauthed(phonenumber)
        db['API_home'].find_one_and_update({'phone_number':phonenumber},{ "$set": {'is_online':True}})
        found_home = Home.objects.get(phone_number=phonenumber)
        home_data = HomeSerializer(found_home, many=False).data
        devices = Device.objects.filter(phone_number=phonenumber)
        res = {"home_id":home_data['phone_number'],'devices':[]}
        device_ord = DeviceOnHomeSerializer(devices, many=True).data
        for d in device_ord:
            res['devices'] += [d]
        return JsonResponse(res, safe=False,  status=status.HTTP_202_ACCEPTED)

    def post(self, request, phonenumber:str):
        if self.request.user.phone_number != phonenumber:
            return self.responseUnauthed(phonenumber)
        db['API_home'].find_one_and_update({'phone_number':phonenumber},{ "$set": {'is_online':True}})
        device_ord = Device.objects.get(_id=ObjectId(request.data['device_id']))
        data_form = {"id":"","name":"","data":"","unit":""}
        if(device_ord.unit == None):
            data_form["unit"] = ""
        else:  data_form["unit"] = device_ord.unit
        data_form["id"] = device_ord.data_id
        data_form["data"] = request.data['data']
        data_form["name"] = device_ord.control_type

        Adafruit.accesses[Adafruit.feedNameToUsername[device_ord.feed_name]].sendDataToFeed(device_ord.feed_name,str(json.dumps(data_form)))

        return JsonResponse(request.data, safe=False,  status=status.HTTP_201_CREATED)
    
class DeviceInfo(SmartHomeAuthView):

    def get(self, request, phonenumber:str, device_id:str):
        device = None
        try:
            device = Device.objects.get(_id=ObjectId(device_id))
        except:
            return JsonResponse(safe=False,  status=status.HTTP_400_BAD_REQUEST, data="Device id not found")

        claimedPhoneNumber = self.request.user.phone_number
        if claimedPhoneNumber != phonenumber or claimedPhoneNumber != device.phone_number:
            return self.responseUnauthed(phonenumber)
        schedules = Schedule.objects.filter(device_id=device_id)
        schedules_serialized = ScheduleDisplaySerializer(schedules,many=True).data
        device_serialized = DeviceDetailSerializer(device, many=False).data
        response = {'device_id': device_id}
        
        response.update(device_serialized)
        response['schedules'] = []
        for sched in schedules_serialized:
            a = {'schedule_id': sched['_id']}
            a.update(dict(sched))
            a['repeat_day'] = literal_eval(a['repeat_day'])
            response['schedules'] += [a]
        return JsonResponse(response, safe=False,  status=status.HTTP_202_ACCEPTED)

@api_view(['GET','POST'])
def addDevice(request):
    """
    demo : i will make  IsAuthencation(request.data[token] in here) in every views funciton
    this thing for test add data
    """
    if request.method == 'POST':
        device = Device()
        device._id = ObjectId()
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
