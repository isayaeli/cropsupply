from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [
    path('checkout-address', views.CheckoutView.as_view(), name='checkout'),
    path('payment/<str:payment_option>', views.swahilies, name='swahilies'),
    path('process/<order_id>', views.process_payment, name='process')
]