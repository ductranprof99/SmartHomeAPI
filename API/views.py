from django.http.response import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import status
from bson.json_util import ObjectId
from API.models import *
from API.serializers import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
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