from django.urls import path
from . import views

urlpatterns = [
    path('reviews', views.product_reviews, name='product_reviews')
]