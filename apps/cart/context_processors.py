from .models import Cart

def cart_total(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {'cart_total': cart.total_items}
    return {'cart_total': 0}