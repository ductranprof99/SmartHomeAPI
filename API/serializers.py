from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import CharField 
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
    device_id = CharField(source='_id')
    class Meta:
        model = Device
        fields = ('device_id', 'device_name', 'device_type', 'description' , 'status','automation_mode')

class DeviceDetailSerializer(serializers.ModelSerializer):
    device_id = CharField(source='_id')
    class Meta:
        model = Device
        fields = ('device_id','device_name', 'device_type', 'description' , 'status','automation_mode','schedules', 'phone_number')


class DeviceCommandSerializer(serializers.ModelSerializer):
     class Meta:
        model = Device
        fields = ('device_id', 'data_id' , 'feed_name','unit','control_type')

class ScheduleDisplaySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Schedule
        fields = ('_id', 'time_on', 'time_off' , 'is_repeat','repeat_day')

class ScheduleInputSerializer(serializers.ModelSerializer):
    schedule_id = CharField(source='_id')
 
    class Meta:
        model = Schedule
        fields = ('schedule_id', 'time_on', 'time_off' , 'is_repeat','repeat_day')

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

