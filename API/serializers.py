from rest_framework import serializers 
from API.models import *
 
 
class HomeSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Home
        fields = '__all__'
