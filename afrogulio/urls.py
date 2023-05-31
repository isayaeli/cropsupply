from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop',views.shop, name='shop'),
    path('product/<int:id>', views.product_details, name='details'),

    path('cart', views.cart, name='cart'),
    path('mini-cart', views.mini_cart, name='mini_cart'),
    path('add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('remove-single-item', views.remove_single_item, name='remove-single-item'),
    path('remove-from-cart', views.remove_from_cart, name='remove_from_cart'),
    path('delete', views.delete_all, name='delete_all'),
]