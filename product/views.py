from django.shortcuts import render,get_object_or_404,redirect
from . models import Product
from django.core .paginator import Paginator
# Create your views here.
def index(request):
    featured_products=Product.objects.order_by('priority')[:4]
    latest_products=Product.objects.order_by('-id')[:4]
    contant={
       'featured_products':featured_products,
       'latest_products':latest_products
    }
    return render(request,'index.html',contant)
def product(request):
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    product_data=Product.objects.order_by('priority')
    product_paginator=Paginator(product_data,4)
    pr=product_paginator.get_page(page)
    
    return render(request,'product.html',{'product':pr})
def productDetails(request,pk):
    
    product = get_object_or_404(Product, pk=pk)
    return render(request,'product_details.html',{'p':product})
def search(request):
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    query=request.GET.get('q')
    if query:
        product=Product.objects.filter(title__icontains=query)
    else:
        product=Product.objects.all()
    if not product:
        product=Product.objects.all()
    product_paginator=Paginator(product,4)
    pr=product_paginator.get_page(page)        
    return render(request,'product.html',{'product':pr})
    
    