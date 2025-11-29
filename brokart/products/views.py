from django.shortcuts import render
from . models import Product
# Create your views here.
from django.core.paginator import Paginator
def index(request):
    return render(request,'index.html')

def list_products(request):
    #returns product list page
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    product_list=Product.objects.all()
    product_paginator=Paginator(product_list,1)
    product_list=product_paginator.get_page(page)
    context={'products':product_list}
    return render(request,'products.html',context)

def detail_product(request):
    return render(request,'product_detail.html')