from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from API.models import *
from API.serializers import *
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['GET'])
def schelude(request,device):
    pass

@api_view(['GET'])
def home(request,home_id):
    if request.method == 'GET':
        # homes = Home.objects.all()
        # homes = homes.filter(address="Ho chi minh")
        # home_data = HomeSerializer(homes, many=True).data
        #a = home_data[0]
        #print(a)

        # home = Home()
        # devicee = {'device_name':'abba','description':'asfasdf','current_status':True,'automation_status':'asfas','mode':1,'schedule':None}
        # home.devices = [devicee,devicee]
        # home.house_name = 'asdfasf'
        # home.address = 'asdfasf'
        # home.save()
        
        print(Home.objects.all())
        return JsonResponse({'a':'a'}, safe=False)

