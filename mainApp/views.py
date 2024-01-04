from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from datetime import datetime


#Slug
from django.utils.text import slugify
import re

def convert_slugify(slug):
    # Remove any non-alphanumeric characters and convert to lowercase
    clean_slug = re.sub(r'[^a-zA-Z0-9]+', '-', slug.lower())
    
    # Remove leading and trailing dashes
    clean_slug = clean_slug.strip('-')
    
    return clean_slug


#Admin Operation Start Here
def login_page(Request):
    if(Request.method=="POST"):
        email=Request.POST.get('email')
        password=Request.POST.get('password')
        user=authenticate(username=email,password=password)
        if(user is not None):
            login(Request,user)
            if (user.is_superuser):
                return redirect('/admin-home')
            else:
                pass

    return render(Request,'login.html')

def logout_page(Request):
    logout(Request)
    return redirect("/login")

@login_required(login_url='/login/')
def admin_home(Request):
    veh=len(Vehicle.objects.all())
    data=Receipt.objects.all().order_by('id').reverse()
    return render(Request,'admin-index.html',{'data':data})


#Maincategory
@login_required(login_url='/login/')
def add_vehicle(Request):
    veh=len(Vehicle.objects.all())
    if(Request.method=="POST"):
        m=Vehicle()
        m.name=Request.POST.get('name')
        m.slug=convert_slugify(m.name)
        m.save()
        return redirect('/vehicle')
    return render(Request,'add-vehicle.html',{'veh':veh})

@login_required(login_url='/login/')
def vehicle_page(Request):
    veh=len(Vehicle.objects.all())
    data=Vehicle.objects.all().order_by('id').reverse()
    return render(Request,'vehicle.html',{'veh':veh,'data':data})

@login_required(login_url='/login/')
def update_vehicle(Request,id):
    veh=len(Vehicle.objects.all())
    data=Vehicle.objects.get(id=id)
    if(Request.method=="POST"):
        data.name=Request.POST.get('name')
        data.slug=convert_slugify(data.name)
        data.save()
        return redirect('/vehicle')
    return render(Request,'update-vehicle.html',{'data':data,'veh':veh})


@login_required(login_url='/login/')
def delete_vehicle(Request,id):
    data=Vehicle.objects.get(id=id)
    data.delete()
    return redirect('/vehicle')

@login_required(login_url='/login/')
def receipt_page(Request):
    return render(Request,'receipt.html')

@login_required(login_url='/login/')
def receipt_list(Request):
    return render(Request,'receipt-page.html')

@login_required(login_url='/login/')
def add_receipt(Request):
    vehicle=Vehicle.objects.all()
    if Request.method=="POST":
        r=Receipt()
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%d/%b/%Y %I:%M %p")
        r.date=formatted_datetime
        r.operator_class=Request.POST.get('operator_class')
        r.amount=int(Request.POST.get('amount'))
        r.save()
        hm=int(r.amount/2)
        
        
        return render(Request,'receipt.html',{'data':r,'hm':hm})

    
    return render(Request,'add-receipt.html',{'vehicle':vehicle})

def home_page(Request):
    return render(Request,'index.html')

def about_page(Request):
    return render(Request,'about.html')

def blog_page(Request):
    return render(Request,'blog.html')

def single_blog_page(Request):
    return render(Request,'blog-single.html')

def contact_page(Request):
    return render(Request,'contact.html')
