from django.shortcuts import render,get_object_or_404,redirect
from product.models import Product
from . models import Order,Orderitem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shopit.settings import LOGIN_URL
# Create your views here.
@login_required(login_url=LOGIN_URL)
def cart(request):
    user=request.user
    customer=user.related_user
    cart_obj,created=Order.objects.get_or_create(
        owners=customer,
        order_status=Order.ORDER_STAGE
    )
    cart_items = cart_obj.related_order.all()
    item=[]
    total=0
    for i in cart_items:
        t=i.quantity*i.product.price
        total+=t
        item.append((i,t))
    return render(request,'cart.html',{'cart':item,'total':total})
@login_required(login_url=LOGIN_URL)
def addCart(request,pk):
    product=get_object_or_404(Product,pk=pk)
    user=request.user
    if not hasattr(user,'related_user'):
        return redirect('login')
    customer=user.related_user
    
    cart_obj,created=Order.objects.get_or_create(
        owners=customer,
        order_status=Order.ORDER_STAGE
        
    )
    exit_item=Orderitem.objects.filter(product=product,owner=cart_obj).exists()
    if not exit_item:
        orderd_item=Orderitem.objects.create(
        product=product,
        quantity=1,
        owner=cart_obj,)
    
    return redirect('cart')
def success(request):
    return render(request,'success.html')

def checkout(request):
    try:
        if request.method=='POST':
            total=request.POST.get('total')
           
            user=request.user
            customer=user.related_user
            order_obj=Order.objects.get(
                owners=customer,
                order_status=Order.ORDER_STAGE
                
            )
            if order_obj:
                order_obj.order_status=Order.ORDER_CONFIRMED
                order_obj.total_price=total
                order_obj.save()
                success_msg="Order Placed Successfully"
                messages.success(request,success_msg)
                return redirect('success')
            else:
                success_msg="Order not Successfully"
                messages.error(request,success_msg)
                
                
                
    except Exception as e:
        success_msg="Order is Not success"
        messages.error(request,success_msg)
       
    return redirect('cart')
    
def remove(request,pk):
    item=Orderitem.objects.get(id=pk)
    item.delete()
    return redirect('cart')
def decrease(request,pk):
    item=get_object_or_404(Orderitem,id=pk)
    if item.quantity!=1:
        item.quantity-=1
        
    item.save()
    return redirect('cart')
def increase(request,pk):
    item=get_object_or_404(Orderitem,id=pk)
    item.quantity+=1
    item.save()
    return redirect('cart')

def orders(request):
    item_list=[]
    order_obj=Order.objects.all()
    for i in order_obj:
        item=i.related_order.all()
        item_list.append(item)
    
    return render(request,'orders.html',{'p':item_list})
def order_search(request):
    user=request.user
    
    customer=user.related_user
    if request.method=='GET':
        query=request.GET.get('q')
        order_obj = Order.objects.filter(
            owners=customer,
            related_order__product__title__icontains=query
            
        ).distinct()
        item_list=[]
        for i in order_obj:
            item=i.related_order.all()
            item_list.append(item)
        
        
            
        
    
    return render(request,'orders.html',{'p':item_list})
    
        
    