from django import template
from afrogulio.models import Cart

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Cart.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0




@register.filter
def cart_items(user):
    if user.is_authenticated:
        qs = Cart.objects.filter(user=user, ordered=False)
        if qs.exists():
            items = qs[0].items.all()
            return items.name
    return 0


