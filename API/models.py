
from djongo import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import int_list_validator



class Schedule(models.Model):
    _id = models.ObjectIdField(primary_key = True)
    time_on = models.CharField(max_length=5,blank=True,null=True)
    time_off = models.CharField(max_length=5,blank=True,null=True)
    is_repeat = models.BooleanField(null=True)
    repeat_day = models.CharField(validators=[int_list_validator],max_length=100)   
    class Meta:
        abstract = True


class Device(models.Model):
    feed_name = models.ObjectIdField(primary_key=True,null=False,blank=False,unique=True)
    device_name = models.CharField(max_length=30,blank=False,null=False)
    description = models.CharField(max_length=50,blank=True,null=True)
    current_status = models.BooleanField(null=False,blank=False)
    automation_status = models.CharField(max_length=50,blank=True,null=True)
    mode = models.IntegerField(null=False,validators=[MaxValueValidator(3),MinValueValidator(1)])
    schedule = models.EmbeddedField(
        model_container=Schedule,
        null=True,
        blank=True
    )
    #history = models.ManyToManyField('History')
    class Meta:
        abstract = True


class Home(models.Model):
    houseID = models.ObjectIdField(primary_key=True)
    house_name = models.CharField(max_length=30,blank=False,null=False)
    address =  models.CharField(max_length=100,blank=False,null=False)
    devices = models.EmbeddedField(
        model_container=Device,
        null=True,
        blank=True
    )


class History(models.Model):
    _id = models.ObjectIdField(primary_key = True)
    time = models.CharField(max_length=30,blank=False,null=False)
    value = models.CharField(max_length=30,blank=False,null=False)
    mode =  models.BooleanField(blank=False,null=False)
    
