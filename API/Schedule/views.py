from django.http.response import JsonResponse
from rest_framework import status
from API.models import *
from API.serializers import *
from ..views import SmartHomeAuthView
from bson.json_util import ObjectId
from ..mongo import db

class ModifySchedule(SmartHomeAuthView):
    def post(self, request):
        """
        this thing for test add data
        """
        data = request.data
        if "schedule_id" in data:
            scheds = Schedule.objects.filter(_id=ObjectId(data['schedule_id']))
            if not scheds:
                return JsonResponse(safe=False,  status=status.HTTP_400_BAD_REQUEST, data="Can't find the schedule")
            sched = scheds.first()
            device_id = sched.device_id
            device = Device.objects.get(_id=ObjectId(device_id))
            if device.phone_number != self.request.user.phone_number:
                return self.responseUnauthed(device.phone_number)
        elif "device_id" in request.data:
            device_id = request.data['device_id']
            device = Device.objects.get(_id=ObjectId(device_id))
            if device.phone_number != self.request.user.phone_number:
                return self.responseUnauthed(device.phone_number)
            sched = Schedule()
            sched.device_id= request.data['device_id']
            sched._id = ObjectId()
        else:
            return JsonResponse(safe=False, status=status.HTTP_400_BAD_REQUEST, data="Possibly wrong data format")

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
            device_id = sched.device_id
            device = Device.objects.get(_id=ObjectId(device_id))
            if device.phone_number != self.request.user.phone_number:
                return self.responseUnauthed(device.phone_number)
            sched.delete()
            return  JsonResponse(safe=False,  status=status.HTTP_202_ACCEPTED, data="Deleted")
        return  JsonResponse(safe=False,  status=status.HTTP_400_BAD_REQUEST, data="Wrong format!")
        
    def patch(self, request):
        if request.data and "device_id" in request.data and "automation_mode" in request.data:
            devices = Device.objects.filter(_id=ObjectId(request.data["device_id"]))
            if devices:
                device = devices.first()
                if device.phone_number != self.request.user.phone_number:
                    return self.responseUnauthed(device.phone_number)
                device.automation_mode = request.data["automation_mode"]
                device.save()
                return  JsonResponse(safe=False,  status=status.HTTP_202_ACCEPTED, data="Updated")
            return  JsonResponse(safe=False,  status=status.HTTP_400_BAD_REQUEST, data="Can't find the device!")
        return  JsonResponse(safe=False,  status=status.HTTP_400_BAD_REQUEST, data="Wrong format!")
