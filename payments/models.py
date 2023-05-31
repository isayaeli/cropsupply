from operator import mod
from django.db import models
from django_countries.fields import CountryField
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class OrderAddress(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    address = models.CharField(max_length=100)
    second_address =models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    placed_on = models.DateTimeField(default=datetime.now)
    order_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username


