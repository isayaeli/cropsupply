from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Product, Cart, CartItem,Deal
admin.site.unregister(Group)
admin.site.site_header = 'Afrogulio Admin'
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Deal)