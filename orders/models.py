from django.db import models
from customers.models  import Customers
from product.models import Product
# Create your models here.
class Order(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICE=((LIVE,'Live'),('Delete',DELETE))
    ORDER_STAGE=0
    ORDER_CONFIRMED=1
    ORDER_PROCESSED=2
    ORDER_DELIVERD=3
    ORDER_REJECTED=4
    STATUS_CHOICE=((ORDER_PROCESSED,'ORDER_PROCESSED'),(ORDER_DELIVERD,'ORDER_DELIVERD'),(ORDER_REJECTED,'ORDER_REJECTED'))
    order_status=models.IntegerField(choices=STATUS_CHOICE,default=ORDER_STAGE)
    
    owners=models.ForeignKey(Customers,on_delete=models.SET_NULL,related_name='orders',null=True)
    total_price=models.FloatField(default=0.0)
    delete_status=models.IntegerField(choices=DELETE_CHOICE,default=LIVE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Orderitem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,related_name='add_cart',null=True)
    quantity=models.IntegerField(default=1)
    owner=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='related_order')