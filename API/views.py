from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from API.models import *
from API.serializers import *
from rest_framework.decorators import api_view
# Create your views here.

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
