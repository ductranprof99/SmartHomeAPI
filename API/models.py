from djongo import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Delete not use field
    username = None
    last_login = None
    is_normaluser = None
    is_superuser = None
    is_online = models.BooleanField(default=False,null=False,blank=False)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, unique=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

class Schedule(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    schedule_id = models.CharField(max_length=24,null=False)
    device_id = models.CharField(max_length=30,blank=False,null=False)
    time_on = models.CharField(max_length=5,blank=True,null=True)
    time_off = models.CharField(max_length=5,blank=True,null=True)
    is_repeat = models.BooleanField(null=True)
    repeat_day = models.CharField(max_length=50,blank=True,null=True)
    objects = models.DjongoManager()


class ScheduleNested(models.Model):
    schedule_id =  models.CharField(max_length=30,blank=False,null=False)
    class Meta:
        abstract = True  


class Device(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    device_id = models.CharField(max_length=24,null=False)
    phone_number =  models.CharField(max_length=30,blank=False,null=False)
    device_name = models.CharField(max_length=30,blank=False,null=False)
    feed_name =  models.CharField(max_length=30,blank=False,null=False)
    description = models.CharField(max_length=50,blank=True,null=True)
    device_type = models.CharField(max_length=30,blank=False,null=False)
    status = models.CharField(max_length=30,blank=False,null=False)
    unit = models.CharField(max_length=30,blank=False,null=False,default="")
    automation_mode = models.IntegerField(null=False,validators=[MaxValueValidator(2),MinValueValidator(0)])
    schedules = models.ArrayField(
        model_container=ScheduleNested,
        null=True,
        blank=True
    )
    objects = models.DjongoManager()
    
class DeviceNested(models.Model):
    device_id =  models.CharField(max_length=30,blank=False,null=False)
    class Meta:
        abstract = True
    

class Home(models.Model):
    home_name = models.CharField(max_length=30,blank=False,null=False)
    phone_number = models.CharField(max_length=30,blank=False,null=False,unique=True,default="required phone number")
    address =  models.CharField(max_length=100,blank=False,null=False)
    is_online = models.BooleanField(default=False,null=False,blank=False)
    devices = models.ArrayField(
        model_container=DeviceNested,
        null=True,
        blank=True
    )
    objects = models.DjongoManager()


class History(models.Model):
    device_id = models.CharField(max_length=30,blank=False,null=False)
    device_type = models.CharField(max_length=10,blank=False,null=False)
    time = models.CharField(max_length=30,blank=False,null=False)
    value = models.CharField(max_length=10,blank=False,null=False)
    unit = models.CharField(max_length=10,blank=False,null=False)
    objects = models.DjongoManager()
