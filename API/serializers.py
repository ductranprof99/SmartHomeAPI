from django.db.models import fields
from rest_framework import serializers 
from API.models import *

 

class AllHomeSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Home
        fields =  ('phone_number', 'address')

class HomeSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Home
        fields = ('phone_number', 'devices')

class HomeDetailSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Home
        fields = '__all__'

class DeviceOnHomeSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Device
        fields = ('device_id', 'device_name', 'description', 'device_type', 'current_status')

class DeviceDetailSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Device
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Schedule
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = History
        fields = '__all__'

        
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}



class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

