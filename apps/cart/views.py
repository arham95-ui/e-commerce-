from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from apps.shop.models import Product
from .models import Cart, CartItem
from firebase import FirestoreDB
from datetime import datetime


def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_detail(request):
    cart = get_or_create_cart(request.user)
    context = {'cart': cart}
    return render(request, 'cart/cart.html', context)


@login_required
@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if not product_id:
        return JsonResponse({'success': False, 'error': 'Product ID required'})
    
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    # Check if AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total_items,
            'message': f'{product.name} added to cart!'
        })
    
    # Non-AJAX redirect
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart:cart_detail')


@login_required
@require_POST
def update_cart_item(request):
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if not item_id:
        return JsonResponse({'success': False, 'error': 'Item ID required'})
    
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()
    
    cart = get_or_create_cart(request.user)
    return JsonResponse({
        'success': True,
        'cart_total': cart.total_items,
        'total_price': float(cart.total_price)
    })


@login_required
@require_POST
def remove_from_cart(request):
    item_id = request.POST.get('item_id')
    
    if not item_id:
        return JsonResponse({'success': False, 'error': 'Item ID required'})
    
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        cart = get_or_create_cart(request.user)
        messages.success(request, 'Item removed from cart.')
        return redirect('cart:cart_detail')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found.')
        return redirect('cart:cart_detail')


@login_required
def checkout(request):
    cart = get_or_create_cart(request.user)
    if cart.total_items == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('shop:home')
    
    if request.method == 'POST':
        # Get user data
        user = request.user
        
        # Get payment method
        payment_method = request.POST.get('payment_method', 'cod')
        
        # Prepare order data
        order_data = {
            'user_id': user.id,
            'user_email': user.email,
            'user_name': user.get_full_name(),
            'user_username': user.username,
            'phone': request.POST.get('phone', ''),
            'address': request.POST.get('address', ''),
            'city': request.POST.get('city', ''),
            'state': request.POST.get('state', ''),
            'zip_code': request.POST.get('zip_code', ''),
            'items': [
                {
                    'product_name': item.product.name,
                    'product_id': item.product.id,
                    'product_price': float(item.product.price),
                    'quantity': item.quantity,
                    'subtotal': float(item.subtotal),
                    'product_image': item.product.image_url or ''
                }
                for item in cart.items.all()
            ],
            'total_amount': float(cart.total_price),
            'payment_method': payment_method,
            'payment_method_display': {
                'cod': 'Cash on Delivery',
                'credit_card': 'Credit/Debit Card',
                'jazzcash': 'JazzCash',
                'easypaisa': 'EasyPaisa',
                'bank_transfer': 'Bank Transfer'
            }.get(payment_method, payment_method),
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Add card details only if credit card
        if payment_method == 'credit_card':
            order_data['card_details'] = {
                'card_number': request.POST.get('card_number', '')[-4:],  # Last 4 digits only
                'card_name': request.POST.get('card_name', ''),
                'expiry_date': request.POST.get('expiry_date', ''),
                'cvv': request.POST.get('cvv', '')  # Store encrypted in production
            }
        else:
            order_data['card_details'] = {}
        
        # Save to Firestore
        try:
            doc_id = FirestoreDB.add_document('orders', order_data)
            if doc_id:
                messages.success(request, '✅ Order placed successfully! Your order has been saved.')
            else:
                messages.warning(request, '⚠️ Order placed but could not save to Firebase.')
        except Exception as e:
            messages.error(request, f'❌ Error saving order: {str(e)}')
            return render(request, 'cart/checkout.html', {'cart': cart})
        
        # Clear cart
        cart.items.all().delete()
        
        return redirect('orders:order_history')
    
    context = {'cart': cart}
    return render(request, 'cart/checkout.html', context)