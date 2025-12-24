from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import Http404
from .models import Order,OrderedItem
from products.models import Product
from customers.models import Customer
# Create your views here.

def show_cart(request):
    context = {}
    context['subtotal'] = 0
    context['tax'] = 0
    context['total'] = 0
    
    if request.user.is_authenticated:
        # Get or create customer profile
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                'name': request.user.username,
                'address': 'Please update your address',
                'phone': '0000000000'
            }
        )
        
        cart = Order.objects.filter(owner=customer, order_status=Order.CART_STAGE).first()
        context['cart'] = cart
        
        # Calculate totals
        if cart:
            subtotal = 0
            for item in cart.added_items.all():
                if item.product:
                    subtotal += item.product.price * item.quantity
            tax = subtotal * 0.10  # 10% tax
            total = subtotal + tax
            context['subtotal'] = subtotal
            context['tax'] = tax
            context['total'] = total
        
        if created:
            messages.info(request, 'Welcome! Please update your profile information in your account settings.')
    else:
        context['cart'] = None
    return render(request,'cart.html', context)
 

def add_to_cart(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to add items to cart')
        return redirect('cart')
    
    if request.method == 'POST':
        user = request.user
        
        # Get or create customer profile
        customer, customer_created = Customer.objects.get_or_create(
            user=user,
            defaults={
                'name': user.username,
                'address': 'Please update your address',
                'phone': '0000000000'
            }
        )
        
        product_id = request.POST.get('product_id')
        quantity_str = request.POST.get('quantity', '1')
        
        # Validate product_id
        if not product_id:
            messages.error(request, 'Invalid product. Please try again.')
            return redirect('cart')
        
        try:
            quantity = int(quantity_str)
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
        
        # Get or create cart
        cart_obj, cart_created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        
        # Get product
        try:
            product = get_object_or_404(Product, pk=product_id)
        except Http404:
            messages.error(request, 'Product not found.')
            return redirect('cart')
        
        # Check if item already exists in cart
        ordered_item, item_created = OrderedItem.objects.get_or_create(
            product=product,
            owner=cart_obj,
            defaults={'quantity': quantity}
        )
        
        if not item_created:
            # Item already exists, update quantity
            ordered_item.quantity += quantity
            ordered_item.save()
            messages.success(request, f'Cart updated. {quantity} more item(s) added.')
        else:
            messages.success(request, 'Item added to cart successfully')
    
    return redirect('cart')


def remove_from_cart(request, item_id):
    """Remove an item from the cart"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to manage your cart')
        return redirect('cart')
    
    try:
        # Get customer profile
        customer, _ = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                'name': request.user.username,
                'address': 'Please update your address',
                'phone': '0000000000'
            }
        )
        
        # Get the cart
        cart = Order.objects.filter(owner=customer, order_status=Order.CART_STAGE).first()
        
        if not cart:
            messages.error(request, 'Cart not found')
            return redirect('cart')
        
        # Get the ordered item
        try:
            ordered_item = OrderedItem.objects.get(pk=item_id, owner=cart)
            product_title = ordered_item.product.title if ordered_item.product else 'Item'
            ordered_item.delete()
            messages.success(request, f'{product_title} removed from cart successfully')
        except OrderedItem.DoesNotExist:
            messages.error(request, 'Item not found in cart')
        
    except Exception as e:
        messages.error(request, 'An error occurred while removing item from cart')
    
    return redirect('cart')
        
