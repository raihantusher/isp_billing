from django.db import models
from django.contrib.auth.models import User
from package.models import Package


# Create your models here.

class Bill(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    due = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    due_date = models.DateTimeField(auto_now_add=True)
    paid_date = models.DateTimeField(auto_now=False)
