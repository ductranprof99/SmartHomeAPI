from rest_framework import serializers 
from API.models import *
 
 
 
class HomeSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Home
        fields = '__all__'

class DevicesAdminSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = DevicesAdmin
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
