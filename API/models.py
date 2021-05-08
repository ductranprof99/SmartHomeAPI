from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class House(models.Model):
    phoneNumber = models.CharField(max_length=20,null=False,blank=False,unique=True)
    name = models.CharField(max_length=100,null=False,blank=False,unique=True)
    password = models.CharField(max_length=50,null=False,blank=False)
    address = models.CharField(max_length=50)


    