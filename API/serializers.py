from rest_framework import serializers 
from API.models import *
 
 
class HouseSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = House
        fields = '__all__'
