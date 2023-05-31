from .models import Cart, CartItem

def afro_context(request):
    try:
        cart = Cart.objects.get(user=request.user, ordered=False)
    except:
        cart = ''
    
    afro_context ={
        'cart':cart
    }
    return  afro_context