from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from . models import Customers
from django.contrib import messages
# Create your views here.
def register(request):
    if request.method=='POST':
        try:
            
        
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')
            address=request.POST.get('address')
            phone=request.POST.get('phone')
            user=User.objects.create_user(
                username=username,
                email=email,
                password=password  
            )
            customers=Customers.objects.create(
                user=user,
                address=address,
                phone=phone
            )
            return redirect('index')
        except Exception as e:
            error_msg="Invalid"
            messages.error(request,error_msg)
            
    return render(request,'register.html')
def loginView(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user=authenticate(username=username,password=password)
        
        if user:
            login(request,user)
            return redirect('index')
        else:
            msg="Invalid login card"
            messages.error(request,msg)
            return render(request,'login.html')
        
    return render(request,'login.html')
def logoutView(request):
    logout(request)
    return redirect('login')
