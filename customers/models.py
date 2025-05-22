from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customers(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICE = (
        (LIVE, 'Live'),
        (DELETE, 'Delete'),
    )
    name=models.CharField(max_length=100,null=True)
    address=models.TextField()
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='related_user')
    phone=models.CharField(max_length=10)
    priority=models.IntegerField(default=0)
    delete_status=models.IntegerField(choices=DELETE_CHOICE,default=LIVE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

