
from enum import unique
from djongo import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import int_list_validator



class Schedule(models.Model):
    time_on = models.CharField(max_length=5,blank=True,null=True)
    time_off = models.CharField(max_length=5,blank=True,null=True)
    is_repeat = models.BooleanField(null=True)
    repeat_day = models.CharField(max_length=50,blank=True,null=True)
    class Meta:
        abstract = True  



class Device(models.Model):
    device_name = models.CharField(max_length=30,blank=False,null=False)
    feed_name =  models.CharField(max_length=30,blank=False,null=False)
    description = models.CharField(max_length=50,blank=True,null=True)
    device_type = models.CharField(max_length=30,blank=False,null=False)
    current_status = models.BooleanField(null=False,blank=False)
    value = models.CharField(max_length=50,blank=True,null=True)
    mode = models.IntegerField(null=False,validators=[MaxValueValidator(3),MinValueValidator(1)])
    schedule = models.ArrayField(
        model_container=Schedule,
        null=True,
        blank=True
    )
    class Meta:
        abstract = True
    


class Home(models.Model):
    _id = models.ObjectIdField(db_column="_id", primary_key=True)
    home_name = models.CharField(max_length=30,blank=False,null=False)
    phone_number = models.CharField(max_length=30,blank=False,null=False,unique=True,default="required phone number")
    address =  models.CharField(max_length=100,blank=False,null=False)
    devices = models.ArrayField(
        model_container=Device,
        null=True,
        blank=True
    )
    objects = models.DjongoManager()


class History(models.Model):
    device_id = models.CharField(max_length=30,blank=False,null=False,default="Need a string there")
    time = models.CharField(max_length=30,blank=False,null=False)
    value = models.CharField(max_length=30,blank=False,null=False)
    mode =  models.BooleanField(blank=False,null=False)
    objects = models.DjongoManager()
    
class DevicesAdmin(models.Model):
    _id = models.ObjectIdField(db_column="_id", primary_key=True)
    home_id = models.CharField(max_length=30,blank=False,null=False)
    objects = models.DjongoManager()