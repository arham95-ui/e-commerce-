from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Order

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'orders/order_history.html', context)

@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)

@login_required
def cancel_order(request, order_number):
    if request.method == 'POST':
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            messages.success(request, 'Order cancelled successfully!')
        else:
            messages.error(request, 'Cannot cancel this order.')
    return redirect('orders:order_history')