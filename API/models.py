from django.db import models
from phone_field import PhoneField
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class User(models.Model):
    phoneNumber = PhoneField(blank=False, help_text='Contact phone number',unique=True)
    password = models.CharField(max_length=50)
    permission = models.BooleanField()