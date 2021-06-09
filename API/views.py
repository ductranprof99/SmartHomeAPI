from django.http.response import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import status
import json
from bson.json_util import ObjectId
from ast import literal_eval

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

class SmartHomeAuthView(APIView):
    permission_classes = (IsAuthenticated,)
    def responseUnauthed(self, id):
        res = {"message": "Unauthorized access to " + id}
        return JsonResponse(res, safe=False,  status=status.HTTP_401_UNAUTHORIZED)
    
class HomeInfo(SmartHomeAuthView):
    def get(self, request):
        phone_number = self.request.user.phone_number
        home = None
        try:
            home = Home.objects.get(phone_number=phone_number)
        except:
            print("ERROR: Error querying home with username: " + phone_number)
        if home:
            home_serialized = HomeDetailSerializer(home, many=False).data
            response = {}
            for field in home_serialized:
                response[field] = home_serialized[field]

        return JsonResponse(response, safe=False,  status=status.HTTP_202_ACCEPTED)
        
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
            response = {"message": "Device id not found"}
            return JsonResponse(response, safe=False,  status=status.HTTP_400_BAD_REQUEST)

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

#TODO CHECK PERMISSION FIRST
class ModifySchedule(SmartHomeAuthView):
    def post(self, request):
        """
        this thing for test add data
        """
        data = request.data
        if "schedule_id" in data:
            scheds = Schedule.objects.filter(_id=ObjectId(data['schedule_id']))
            if not scheds:
                return  JsonResponse(safe=False,  status=status.HTTP_400_BAD_REQUEST, data="Can't find the schedule")
            sched = scheds.first()
        else:
            sched = Schedule()
            sched.device_id= request.data['device_id']
            sched._id = ObjectId()

        sched.is_repeat = request.data['is_repeat']
        sched.repeat_day = str(request.data['repeat_day'])
        sched.time_on = request.data['time_on']
        sched.time_off = request.data['time_off']
        sched.save()
        sched_serialized = ScheduleInputSerializer(sched).data

        return  JsonResponse(sched_serialized, safe=False,  status=status.HTTP_202_ACCEPTED)
        
    def delete(self, request):
        if request.data and "schedule_id" in request.data:
            scheds = Schedule.objects.filter(_id=ObjectId(request.data['schedule_id']))
            if not scheds:
                return  JsonResponse(safe=False,  status=status.HTTP_400_BAD_REQUEST, data="Can't find the schedule")
            sched = scheds.first()
            sched.delete()
        return  JsonResponse(safe=False,  status=status.HTTP_202_ACCEPTED, data="Deleted")
