from socket import timeout
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length = 100)
    image = models.FileField(upload_to='product_images')
    price = models.IntegerField()
    discount_price = models.CharField(max_length=100, null=True, blank=True)
    details =  models.TextField()

    def __str__(self):
        return self.title


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True)
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.quantity} of {self.product.title}"
    
    def get_total_price(self):
        return self.product.price * self.quantity

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, related_name='items' ,blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    @property
    def get_line_total(self):
        total = 0
        try:
            for cart_item in self.items.all():
                total = int(total + cart_item.get_total_price())
            return total
        except:
            return 0
    
class Deal(models.Model):
    image = models.FileField(upload_to='deals_images')
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    deadline = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.title