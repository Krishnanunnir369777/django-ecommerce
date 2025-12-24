from django.shortcuts import render, get_object_or_404
from . models import Product, Category
from django.db.models import Q
# Create your views here.
from django.core.paginator import Paginator

def index(request):
    featured_products = Product.objects.filter(delete_status=Product.LIVE).order_by('priority')[:4]
    latest_products = Product.objects.filter(delete_status=Product.LIVE).order_by('-id')[:4]
    categories = Category.objects.filter(delete_status=Category.LIVE)[:3]
    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories
    }
    return render(request,'index.html',context)

def list_products(request):
    #returns product list page with search and filter
    products = Product.objects.filter(delete_status=Product.LIVE)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Category filter
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Price filter
    price_filter = request.GET.get('price', '')
    if price_filter == 'low':
        products = products.order_by('price')
    elif price_filter == 'high':
        products = products.order_by('-price')
    else:
        products = products.order_by('-priority', '-id')
    
    # Pagination
    page = request.GET.get('page', 1)
    product_paginator = Paginator(products, 12)  # Show 12 products per page
    product_list = product_paginator.get_page(page)
    
    categories = Category.objects.filter(delete_status=Category.LIVE)
    context = {
        'products': product_list,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_price': price_filter
    }
    return render(request,'products.html',context)

def detail_product(request, pk):
    product = get_object_or_404(Product, pk=pk, delete_status=Product.LIVE)
    # Get related products from same category
    related_products = Product.objects.filter(
        category=product.category,
        delete_status=Product.LIVE
    ).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request,'product_detail.html',context)