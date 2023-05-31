
from email import header
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
import requests
import math
import random
from django.conf import settings
from payments.models import OrderAddress
from . forms import checkoutForm
from afrogulio.models import Cart

key = settings.SWAHILIES_SECRET_KEY
url = "https://swahiliesapi.invict.site/Api"
headers = {'User-Agent': 'Mozilla/5.0'}

# Create your views here.
class CheckoutView(View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user, ordered=False)
        form = checkoutForm()
        context={
           'form':form,
           'cart':cart
        }
        return render(self.request, 'payments/checkout.html', context)
    def post(self,*args, **kwargs):
        print(self.request.POST)
        form = checkoutForm(self.request.POST or None)
        try:
            cart = Cart.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                address = form.cleaned_data.get('address')
                second_address = form.cleaned_data.get('second_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                phone = form.cleaned_data.get('phone')
                email = form.cleaned_data.get('email')
                payment = form.cleaned_data.get('payment')
                order_id = ''+str(math.floor(1000000 + random.random()*9000000)),
                order = OrderAddress(
                    user= self.request.user,
                    address= address,
                    second_address= second_address,
                    country=country,
                    zip_code=zip_code,
                    phone= phone,
                    email= email,
                    order_id = order_id

                )
                order.save()
                # cart.ordered = True
                # cart.order = order
                # cart.save()
                # send_mail(
                #     'New Order has been placed',
                #     f"Please visit your admin panel site to see order",
                #     'ummasoft@gmail.com',['isayaelib@gmail.com'], fail_silently=False
                # )
                if payment == 'S':
                     return redirect('process', order_id=order_id)
                elif payment == 'C':
                    return redirect('payment', payment_option='cash')
                else:
                    messages.warning(self.request, "Ivalid payment method")
            messages.info(self.request, "Failed checkout")
            return redirect('checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order..")
            return redirect('cart')



def swahilies(request, payment_option):

    return render(request, 'payments/swahilies.html')


def process_payment(request, order_id):
    cart = Cart.objects.get(user=request.user, ordered=False)
    payload = {
        "api":170, "code":101,"data":{
        "api_key":key,
        "order_id": order_id,
        "amount":cart.get_line_total,
        "username":"Afrogulio",
        "phone_number":"0783262616",
        "is_live":False,
        # "cancel_url": "afrogulio.co.tz/canceled"
        }}
    response = requests.post(url,  headers=headers, json=payload)
    # print(response.json())
    response =response.json()
    # print(response['code'])
    return redirect(response['payment_url'])
   

def reconcilliation(request):
    payload = {"api":170, "code":103,"data":{
        "api_key":key
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())
    response =response.json()
    print(response['code'])
    
