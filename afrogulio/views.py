from django.shortcuts import redirect, render, get_object_or_404
from django.http.response import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.contrib import messages
from django.db.models import Count
from .models import Product
from .models import Cart, CartItem, Deal
from rating.models import Product_Rating
# Create your views here.

def home(request):
    products = Product.objects.all().order_by('-id')[:10]
    deals = Deal.objects.all()
    context = {
        'products':products,
        'deals':deals
    }
    return render(request, 'afrogulio/home.html', context)

def shop(request):
    products = Product.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product =paginator.page(paginator.num_pages)
    context = {
        'products':products, 
        'product':product
    }
    return render(request, 'afrogulio/shop.html', context)


def product_details(request,id):
    product =get_object_or_404(Product, id=id)
    products = Product.objects.all().order_by('-id')
    mycart = 0
    try:
        cart = Cart.objects.get(user=request.user, ordered=False)
        qs=  cart.items.filter(product__id=product.id).exists()
        if qs:
            cart_item , created = CartItem.objects.get_or_create(
            product=product,
            user= request.user,
            )
            mycart = cart_item  
    except:
        mycart = 0
    
    rating = Product_Rating.objects.filter(rating_for=product.id)
    sum_of_user_rates =  sum(rating.values_list('rating_value', flat=True)) # --> rating for one user filtered above

    all_ratings_to_talent = rating.count()  * 5 # --> getting number of all ratings for a filtered user
    try:
       rates= round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
    except ZeroDivisionError:
        rates = 0
        
    ratings =  Product_Rating.objects.filter(rating_for=product.id).annotate(count = Count('rating_value'))
    all_ratings =  Product_Rating.objects.filter(rating_for=product.id)

    page = request.GET.get('page', 1)
    paginator = Paginator(all_ratings, 2)
    try:
        rating_list = paginator.page(page)
    except PageNotAnInteger:
        rating_list = paginator.page(1)
    except EmptyPage:
        rating_list =paginator.page(paginator.num_pages)


    context = {
        'data':product,
        'mycart':mycart,
        'rates':rates,
        'ratings':ratings,
        'all_ratings':all_ratings,
        'products':products,
        'rating_list':rating_list
    }
    return render(request, 'afrogulio/product_details.html', context)

def cart(request):
    try:
        cart = Cart.objects.get(user=request.user, ordered=False)
    except:
        messages.info(request,"You don't have an active order start by adding product to a cart")
        return redirect('shop')
    
    products = Product.objects.all().order_by('-id')
    context = {
        'cart':cart,
        'products':products
    }
    return render(request, 'afrogulio/cart.html', context)

def mini_cart(request):
    cart = Cart.objects.get(user=request.user, ordered=False)
    response_data = {}
    if request.is_ajax():
        response_data['success'] = "Retrieved"
        for data in cart.items.all():
            response_data['price'] = data.product.price
            response_data['title'] = data.product.title
            response_data['quantity'] = data.quantity
            response_data['image'] = data.product.image.url
            return HttpResponse(
                    json.dumps(response_data),
                    content_type = 'application/json'
                )


def add_to_cart(request):
    if request.method == 'POST':
        print(request.POST)
        p_id = request.POST['p_id']
        product = get_object_or_404(Product, id=p_id)
        response_data = {}
        cart_item , created = CartItem.objects.get_or_create(
            product=product,
            user= request.user,
        )
        cart_qs = Cart.objects.filter(user=request.user, ordered=False)
        if cart_qs.exists():
            cart = cart_qs[0]
            if cart.items.filter(product_id =product.id).exists():
                cart_item.quantity +=1
                cart_item.save()
                response_data['success'] = 'Successfull updated'
                response_data['quantity'] = cart_item.quantity
                response_data['total'] = cart.get_line_total
                response_data['price'] = cart_item.product.price
                response_data['count'] = cart.items.count()
                response_data['id'] = cart_item.product.id
                return HttpResponse(
                    json.dumps(response_data),
                    content_type = 'application/json'
                )
            else:
                cart.items.add(cart_item)
                response_data['success'] = 'Successfull added'
                response_data['count'] = cart.items.count()
                response_data['total'] = cart.get_line_total
                response_data['quantity'] = cart_item.quantity
                return HttpResponse(
                    json.dumps(response_data),
                    content_type = 'application/json'
                )
        else:
            cart = Cart.objects.create(user=request.user)
            cart.items.add(cart_item)
            response_data['success'] = 'Successfull created'
            response_data['quantity'] = cart_item.quantity
            response_data['total'] = cart.get_line_total
            response_data['price'] = cart_item.product.price
            response_data['count'] = cart.items.count()
            response_data['id'] = cart_item.product.id
            return HttpResponse(
                    json.dumps(response_data),
                    content_type = 'application/json'
                )


def remove_single_item(request):
    if request.method == 'POST':
        print(request.POST)
        p_id = request.POST['p_id']
        product = get_object_or_404(Product, id=p_id)
        response_data = {}
        cart_item , created = CartItem.objects.get_or_create(
            product=product,
            user= request.user,
            ordered = False
        )
        cart_qs = Cart.objects.filter(user=request.user, ordered=False)
        if cart_qs.exists():
            cart = cart_qs[0]
            if cart.items.filter(product_id =product.id).exists():
                cart_item.quantity -=1
                cart_item.save()
                response_data['success'] = 'Successfull updated'
                response_data['quantity'] = cart_item.quantity
                response_data['total'] = cart.get_line_total
                response_data['price'] = cart_item.product.price
                response_data['id'] = cart_item.product.id
                return HttpResponse(
                    json.dumps(response_data),
                    content_type = 'application/json'
                )
            else:
                cart.items.add(cart_item)
                response_data['success'] = 'Successfull added'
                return HttpResponse(
                    json.dumps(response_data),
                    content_type = 'application/json'
                )
        else:
            cart = Cart.objects.create(user=request.user)
            cart.items.add(cart_item)
            response_data['success'] = 'Successfull created'
            return HttpResponse(
                    json.dumps(response_data),
                    content_type = 'application/json'
                )
    
   

def remove_from_cart(request):
    if request.method == 'POST':
        p_id = request.POST['p_id']
        product = get_object_or_404(Product, id=p_id)
        response_data = {}
        cart_qs = Cart.objects.filter(user=request.user, ordered=False)
        if cart_qs.exists():
            cart = cart_qs[0]
            cart_item = CartItem.objects.filter(
            product=product,
            user=request.user,
            ordered=False
            )[0]
            cart.items.remove(cart_item)
            response_data['success'] = 'Successfull Removed '
            response_data['count'] = cart.items.count()
            response_data['total'] = cart.get_line_total
            return HttpResponse(
                json.dumps(response_data),
                content_type = 'application/json'
            )
        else:
            response_data['success'] = 'No Product in your cart'
            return HttpResponse(
                json.dumps(response_data),
                content_type = 'application/json'
            )
    else:
        response_data['success'] = 'You do not have an active order'
        return HttpResponse(
                json.dumps(response_data),
                content_type = 'application/json'
            )




def delete_all(request):
    cart  = Cart.objects.get(user=request.user, ordered=False)
    items = CartItem.objects.filter(user=request.user, cart=cart)
    cart.delete(items)
    return redirect('cart')
        