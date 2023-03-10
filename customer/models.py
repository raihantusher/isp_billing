from django.db import models
# Create your models here.

class Customer(models.Model):
    full_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=14)
    pppoe_username = models.CharField(max_length=25)
    pppoe_password = models.CharField(max_length=25)

class Area(models.Model):
    area_name = models.CharField(max_length=25)