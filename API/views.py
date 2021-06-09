from django.http.response import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import status
import json
from bson.json_util import ObjectId

from API.models import *
from API.serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from API import Adafruit
from rest_framework.permissions import IsAuthenticated

from .mongo import db


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

class DeviceList(APIView):
    permission_classes = (IsAuthenticated,)
    
    def responseUnauthed(self, id):
        res = {"message": "Unauthorized access to " + id}
        return JsonResponse(res, safe=False,  status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, phonenumber:str):
        if self.request.user.phone_number != phonenumber:
            return self.responseUnauthed(phonenumber)
        db['API_home'].find_one_and_update({'phone_number':phonenumber},{ "$set": {'is_online':True}})
        found_home = Home.objects.get(phone_number=phonenumber)
        home_data = HomeSerializer(found_home, many=False).data
        devices = Device.objects.filter(phone_number=phonenumber)
        if request.method == 'GET':
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

@api_view(['GET','POST'])
def addSchedule(request):
    """
    this thing for test add data
    """
    if request.method == 'POST':
        sched = Schedule()
        sched._id = ObjectId()
        sched.schedule_id = str(sched._id)
        sched.is_repeat = request.data['is_repeat']
        sched.repeat_day = str(request.data['repeat_day'])
        sched.time_on = request.data['time_on']
        sched.time_off = request.data['time_off']
        sched.save()
        print(sched)
        return  JsonResponse({'a':'a'}, safe=False,  status=status.HTTP_202_ACCEPTED)