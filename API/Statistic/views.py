import json
from django.http.response import JsonResponse
from rest_framework import status
from API.models import *
from API.serializers import *
from ..views import SmartHomeAuthView
from .. import analizer


class StatisticManager(SmartHomeAuthView):
    
    def get(self, request):
        ajaxpreload = analizer.Statistic()

        claimedPhoneNumber = self.request.user.phone_number
        try:
            Home.objects.get(phone_number=claimedPhoneNumber)
        except:
            return self.responseUnauthed(claimedPhoneNumber)
        device_type = self.request.query_params.get('device-type')
        range_date = self.request.query_params.get('range')
        # change this later for custom range
        if range_date == 'week':
            result = ajaxpreload.calculate(claimedPhoneNumber,1,None,device_type)
            return JsonResponse(result, safe=False,  status=status.HTTP_202_ACCEPTED)
        elif range_date == 'month':
            result = ajaxpreload.calculate(claimedPhoneNumber,None,1,device_type)
            return JsonResponse(result, safe=False,  status=status.HTTP_202_ACCEPTED)
        return JsonResponse({}, safe=False,  status=status.HTTP_404_NOT_FOUND)

