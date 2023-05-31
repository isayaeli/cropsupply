from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from afrogulio.models import Product

# Create your models here.

class Product_Rating(models.Model):
    rating_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_for =  models.ForeignKey(Product, on_delete=models.CASCADE)
    rating_date = models.DateTimeField(default=datetime.now)
    rating_value = models.FloatField(max_length=100)
    comments = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return str(self.rating_for)