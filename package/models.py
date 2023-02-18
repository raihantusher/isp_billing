from django.db import models

# Create your models here.

class Package(models.Model):
    package_name = models.CharField(max_length=200)
    price = models.DecimalField(default=0)