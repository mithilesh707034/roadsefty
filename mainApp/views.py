from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from datetime import datetime
import pytz
from django.http import HttpResponseForbidden
from decimal import Decimal


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
                if(Branch.objects.filter(email=email)):
                  return redirect('/branch-home')
                else:
                    return redirect('/employee-home')


    return render(Request,'login.html')

def logout_page(Request):
    logout(Request)
    return redirect("/login")

@login_required(login_url='/login/')
def admin_home(Request):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        tt = Decimal(0)
        shift_totals = {'1': Decimal(0), '2': Decimal(0), '3': Decimal(0)}
        
        data = Receipt.objects.all().order_by('id').reverse()
        current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_datetime_ist = current_datetime_utc.astimezone(indian_timezone)
        formatted_date = current_datetime_ist.strftime("%d/%b/%Y")
        
        t = Receipt.objects.filter(date__startswith=formatted_date)
        
        for i in t:
            tt += Decimal(i.amount)
            shift_totals[i.shift_name] = shift_totals.get(i.shift_name, Decimal(0)) + Decimal(i.amount)
        
        # Now shift_totals contains the total amount for each shift, even if the shift name is not present in the Receipt objects
        s1 = shift_totals.get('01', Decimal(0))
        s2 = shift_totals.get('02', Decimal(0))
        s3 = shift_totals.get('03', Decimal(0))
        return render(Request,'admin-index.html',{'data':t,'tt':tt,'s1':s1,'s2':s2,'s3':s3})

@login_required(login_url='/login/')
def admin_filter_receipt(Request,email):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        tt = Decimal(0)
        shift_totals = {'1': Decimal(0), '2': Decimal(0), '3': Decimal(0)}
        
        data = Receipt.objects.all().order_by('id').reverse()
        current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_datetime_ist = current_datetime_utc.astimezone(indian_timezone)
        formatted_date = current_datetime_ist.strftime("%d/%b/%Y")
        
        t = Receipt.objects.filter(date__startswith=formatted_date,branch_email=email)
        
        for i in t:
            tt += Decimal(i.amount)
            shift_totals[i.shift_name] = shift_totals.get(i.shift_name, Decimal(0)) + Decimal(i.amount)
        
        # Now shift_totals contains the total amount for each shift, even if the shift name is not present in the Receipt objects
        s1 = shift_totals.get('01', Decimal(0))
        s2 = shift_totals.get('02', Decimal(0))
        s3 = shift_totals.get('03', Decimal(0))
        return render(Request,'admin-index.html',{'data':t,'tt':tt,'s1':s1,'s2':s2,'s3':s3})



@login_required(login_url='/login/')
def total_receipt(Request):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
      tt = Decimal(0)
      shift_totals = {'1': Decimal(0), '2': Decimal(0), '3': Decimal(0)}
      if Request.method == "POST":
         from_date_str = Request.POST.get('from_date')
         to_date_str = Request.POST.get('to_date')
         
         # Convert string dates to datetime objects
         from_date = datetime.strptime(from_date_str, '%Y-%m-%d').replace(tzinfo=pytz.timezone('Asia/Kolkata'))
         to_date = datetime.strptime(to_date_str, '%Y-%m-%d').replace(tzinfo=pytz.timezone('Asia/Kolkata'))
         
         # Print only the date part
         from_date_tl = from_date.strftime('%d/%b/%Y %I:%M %p')
         to_date_tl = to_date.strftime('%d/%b/%Y %I:%M %p')
         
         print("From Date:", from_date_tl, "To Date:", to_date_tl)
         
         # Filter data between from_date and to_date (inclusive)
         data = Receipt.objects.filter(date__range=[from_date_tl, to_date_tl]).order_by('id').reverse()
     
         # ... rest of your code ...
         if data:
             print("Hi")
     
         for i in data:
             tt += Decimal(i.amount)
             shift_totals[i.shift_name] = shift_totals.get(i.shift_name, Decimal(0)) + Decimal(i.amount)
    
         # Now shift_totals contains the total amount for each shift within the specified date range
         s1 = shift_totals.get('01', Decimal(0))
         s2 = shift_totals.get('02', Decimal(0))
         s3 = shift_totals.get('03', Decimal(0))
        
            
      else:
        tt = Decimal(0)
        shift_totals = {'1': Decimal(0), '2': Decimal(0), '3': Decimal(0)}
        
        data = Receipt.objects.all().order_by('id').reverse()
        current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_datetime_ist = current_datetime_utc.astimezone(indian_timezone)
        formatted_date = current_datetime_ist.strftime("%d/%b/%Y")
        
        t = Receipt.objects.all()
        
        for i in t:
            tt += Decimal(i.amount)
            shift_totals[i.shift_name] = shift_totals.get(i.shift_name, Decimal(0)) + Decimal(i.amount)
        
        # Now shift_totals contains the total amount for each shift, even if the shift name is not present in the Receipt objects
        s1 = shift_totals.get('01', Decimal(0))
        s2 = shift_totals.get('02', Decimal(0))
        s3 = shift_totals.get('03', Decimal(0))
      return render(Request,'total-receipt.html',{'data':data,'tt':tt,'s1':s1,'s2':s2,'s3':s3})



#Maincategory
@login_required(login_url='/login/')
def add_vehicle(Request):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       veh=len(Vehicle.objects.all())
       if(Request.method=="POST"):
           m=Vehicle()
           m.name=Request.POST.get('name')
           m.slug=convert_slugify(m.name)
           m.price=int(Request.POST.get('price'))
           m.save()
           return redirect('/vehicle')
       return render(Request,'add-vehicle.html',{'veh':veh})

@login_required(login_url='/login/')
def vehicle_page(Request):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       veh=len(Vehicle.objects.all())
       data=Vehicle.objects.all().order_by('id').reverse()
       return render(Request,'vehicle.html',{'veh':veh,'data':data})

@login_required(login_url='/login/')
def update_vehicle(Request,id):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       veh=len(Vehicle.objects.all())
       data=Vehicle.objects.get(id=id)
       if(Request.method=="POST"):
           data.name=Request.POST.get('name')
           data.slug=convert_slugify(data.name)
           data.price=int(Request.POST.get('price'))
           data.save()
           return redirect('/vehicle')
       return render(Request,'update-vehicle.html',{'data':data,'veh':veh})


@login_required(login_url='/login/')
def delete_vehicle(Request,id):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       data=Vehicle.objects.get(id=id)
       data.delete()
       return redirect('/vehicle')

@login_required(login_url='/login/')
def receipt_page(Request):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       return render(Request,'receipt.html')

@login_required(login_url='/login/')
def receipt_list(Request):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       return render(Request,'receipt-page.html')

@login_required(login_url='/login/')
def add_receipt(Request):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        vehicle=Vehicle.objects.all()
        if Request.method=="POST":
            r=Receipt()
            current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)

            # Convert UTC time to Indian Standard Time (IST)
            indian_timezone = pytz.timezone('Asia/Kolkata')
            current_datetime_ist = current_datetime_utc.astimezone(indian_timezone)
            
            # Format the date and time as required in IST
            formatted_datetime = current_datetime_ist.strftime("%d/%b/%Y %I:%M %p")
            
            # Create a Receipt instance
            r = Receipt()
            r.date = formatted_datetime
            r.operator_class = Request.POST.get('operator_class')
            r.vehicle_number = Request.POST.get('vehicle_number')
            
            # Define shift timings
            shift_timings = {
                '01': (datetime.strptime('00:00', '%H:%M'), datetime.strptime('07:59', '%H:%M')),
                '02': (datetime.strptime('08:00', '%H:%M'), datetime.strptime('15:59', '%H:%M')),
                '03': (datetime.strptime('16:00', '%H:%M'), datetime.strptime('23:59', '%H:%M'))
            }
            
            # Determine the shift based on current time
            current_time = current_datetime_ist.time()
            for shift_name, (start_time, end_time) in shift_timings.items():
                start_time = start_time.time()
                end_time = end_time.time()
                if start_time <= current_time <= end_time:
                    r.shift_name = shift_name
                    break
            else:
                # Handle the case where the current time does not fall into any shift
                r.shift_name = 'Unknown'
            
            # Use r.shift_name as needed
            try:
                v=Vehicle.objects.get(name=r.operator_class)
                r.amount=v.price
            except:
                pass
            
            r.save()
            hm=int(r.amount/2)
    
    
            return render(Request,'receipt.html',{'data':r,'hm':hm})


    return render(Request,'add-receipt.html',{'vehicle':vehicle})


@login_required(login_url='/login/')
def delete_receipt(Request,id):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       data=Receipt.objects.get(id=id)
       data.delete()
       return redirect('/admin-home')
    


    
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

def contact_page(Request):
    return render(Request,'contact.html')

def not_found(Request,name):
    return render(Request,'404.html')



@login_required(login_url='/login/')
def add_branch(Request):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       uname=User.objects.all()
       if(Request.method=="POST"):
           b=Branch()
           b.name=Request.POST.get('name')
           b.email=Request.POST.get('email')
           b.password=Request.POST.get('password')
           b.address=Request.POST.get('address')
           try:
                u=Branch.objects.get(username=b.email)
                if(u):
                   pass
           except:
                   user = User(username=b.email, email=b.email,first_name=b.name)
                   if (user):
                       user.set_password(b.password)
                       user.save()
                       b.save()
                       return redirect('/branch')
       return render(Request,'add-branch.html',{'uname':uname})

@login_required(login_url='/login/')
def branch_page(Request):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       data=Branch.objects.all().order_by('id').reverse()
       return render(Request,'branch.html',{'data':data})

@login_required(login_url='/login/')
def update_branch(Request,id):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       
       data=Branch.objects.get(id=id)
       if(Request.method=="POST"):
           data.name=Request.POST.get('name')
           data.address=Request.POST.get('address')
           data.save()
           return redirect('/branch')
       return render(Request,'update-branch.html',{'data':data})


@login_required(login_url='/login/')
def delete_branch(Request,id):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       data=Branch.objects.get(id=id)
       u=User.objects.get(username=data.email)
       if(u):
         u.delete()
       data.delete()
       return redirect('/branch')


@login_required(login_url='/login/')
def branch_home(Request):
    if Branch.objects.filter(email=Request.user.username):
    
        tt = Decimal(0)
        shift_totals = {'1': Decimal(0), '2': Decimal(0), '3': Decimal(0)}
        
        data = Receipt.objects.all().order_by('id').reverse()
        current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_datetime_ist = current_datetime_utc.astimezone(indian_timezone)
        formatted_date = current_datetime_ist.strftime("%d/%b/%Y")
        
        t = Receipt.objects.filter(date__startswith=formatted_date,branch_email=Request.user.username)
        
        for i in t:
            tt += Decimal(i.amount)
            shift_totals[i.shift_name] = shift_totals.get(i.shift_name, Decimal(0)) + Decimal(i.amount)
        
        # Now shift_totals contains the total amount for each shift, even if the shift name is not present in the Receipt objects
        s1 = shift_totals.get('01', Decimal(0))
        s2 = shift_totals.get('02', Decimal(0))
        s3 = shift_totals.get('03', Decimal(0))
        return render(Request,'branch/branch-index.html',{'data':t,'tt':tt,'s1':s1,'s2':s2,'s3':s3})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")

@login_required(login_url='/login/')
def branch_filter_employee_receipt(Request,email):
    if Branch.objects.filter(email=Request.user.username):
    
        tt = Decimal(0)
        shift_totals = {'1': Decimal(0), '2': Decimal(0), '3': Decimal(0)}
        
        data = Receipt.objects.all().order_by('id').reverse()
        current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_datetime_ist = current_datetime_utc.astimezone(indian_timezone)
        formatted_date = current_datetime_ist.strftime("%d/%b/%Y")
        
        t = Receipt.objects.filter(date__startswith=formatted_date,employee_email=email)
        
        for i in t:
            tt += Decimal(i.amount)
            shift_totals[i.shift_name] = shift_totals.get(i.shift_name, Decimal(0)) + Decimal(i.amount)
        
        # Now shift_totals contains the total amount for each shift, even if the shift name is not present in the Receipt objects
        s1 = shift_totals.get('01', Decimal(0))
        s2 = shift_totals.get('02', Decimal(0))
        s3 = shift_totals.get('03', Decimal(0))
        return render(Request,'branch/branch-index.html',{'data':t,'tt':tt,'s1':s1,'s2':s2,'s3':s3})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")


@login_required(login_url='/login/')
def branch_total_receipt(Request):
    if Branch.objects.filter(email=Request.user.username):
    
      tt = Decimal(0)
      shift_totals = {'1': Decimal(0), '2': Decimal(0), '3': Decimal(0)}
      if Request.method == "POST":
         from_date_str = Request.POST.get('from_date')
         to_date_str = Request.POST.get('to_date')
         
         # Convert string dates to datetime objects
         from_date = datetime.strptime(from_date_str, '%Y-%m-%d').replace(tzinfo=pytz.timezone('Asia/Kolkata'))
         to_date = datetime.strptime(to_date_str, '%Y-%m-%d').replace(tzinfo=pytz.timezone('Asia/Kolkata'))
         
         # Print only the date part
         from_date_tl = from_date.strftime('%d/%b/%Y %I:%M %p')
         to_date_tl = to_date.strftime('%d/%b/%Y %I:%M %p')
         
         print("From Date:", from_date_tl, "To Date:", to_date_tl)
         
         # Filter data between from_date and to_date (inclusive)
         data = Receipt.objects.filter(date__range=[from_date_tl, to_date_tl],branch_email=Request.user.username).order_by('id').reverse()
     
         # ... rest of your code ...
         if data:
             print("Hi")
     
         for i in data:
             tt += Decimal(i.amount)
             shift_totals[i.shift_name] = shift_totals.get(i.shift_name, Decimal(0)) + Decimal(i.amount)
    
         # Now shift_totals contains the total amount for each shift within the specified date range
         s1 = shift_totals.get('01', Decimal(0))
         s2 = shift_totals.get('02', Decimal(0))
         s3 = shift_totals.get('03', Decimal(0))
        
            
      else:
        tt = Decimal(0)
        shift_totals = {'1': Decimal(0), '2': Decimal(0), '3': Decimal(0)}
        
        data = Receipt.objects.filter(branch_email=Request.user.username).order_by('id').reverse()
        current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_datetime_ist = current_datetime_utc.astimezone(indian_timezone)
        formatted_date = current_datetime_ist.strftime("%d/%b/%Y")
        
        t = Receipt.objects.filter(branch_email=Request.user.username)
        
        for i in t:
            tt += Decimal(i.amount)
            shift_totals[i.shift_name] = shift_totals.get(i.shift_name, Decimal(0)) + Decimal(i.amount)
        
        # Now shift_totals contains the total amount for each shift, even if the shift name is not present in the Receipt objects
        s1 = shift_totals.get('01', Decimal(0))
        s2 = shift_totals.get('02', Decimal(0))
        s3 = shift_totals.get('03', Decimal(0))
      return render(Request,'branch/total-receipt.html',{'data':data,'tt':tt,'s1':s1,'s2':s2,'s3':s3})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")


@login_required(login_url='/login/')
def receipt_page(Request):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       return render(Request,'receipt.html')

@login_required(login_url='/login/')
def receipt_list(Request):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       return render(Request,'receipt-page.html')

@login_required(login_url='/login/')
def add_branch_receipt(Request):
 if Branch.objects.filter(email=Request.user.username):
    
        vehicle=Vehicle.objects.all()
        if Request.method=="POST":
            r=Receipt()
            current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)

            # Convert UTC time to Indian Standard Time (IST)
            indian_timezone = pytz.timezone('Asia/Kolkata')
            current_datetime_ist = current_datetime_utc.astimezone(indian_timezone)
            
            # Format the date and time as required in IST
            formatted_datetime = current_datetime_ist.strftime("%d/%b/%Y %I:%M %p")
            
            # Create a Receipt instance
            r = Receipt()
            r.date = formatted_datetime
            r.operator_class = Request.POST.get('operator_class')
            r.vehicle_number = Request.POST.get('vehicle_number')
            r.branch_email=Request.user.username
            
            # Define shift timings
            shift_timings = {
                '01': (datetime.strptime('00:00', '%H:%M'), datetime.strptime('07:59', '%H:%M')),
                '02': (datetime.strptime('08:00', '%H:%M'), datetime.strptime('15:59', '%H:%M')),
                '03': (datetime.strptime('16:00', '%H:%M'), datetime.strptime('23:59', '%H:%M'))
            }
            
            # Determine the shift based on current time
            current_time = current_datetime_ist.time()
            for shift_name, (start_time, end_time) in shift_timings.items():
                start_time = start_time.time()
                end_time = end_time.time()
                if start_time <= current_time <= end_time:
                    r.shift_name = shift_name
                    break
            else:
                # Handle the case where the current time does not fall into any shift
                r.shift_name = 'Unknown'
            
            # Use r.shift_name as needed
            try:
                v=Vehicle.objects.get(name=r.operator_class)
                r.amount=v.price
            except:
                pass
            
            r.save()
            hm=int(r.amount/2)
    
    
            return render(Request,'receipt.html',{'data':r,'hm':hm})


        return render(Request,'branch/add-receipt.html',{'vehicle':vehicle})
 else:
     return HttpResponseForbidden("You don't have permission to access this page.")


@login_required(login_url='/login/')
def delete_receipt(Request,id):
    if not Request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
       data=Receipt.objects.get(id=id)
       data.delete()
       return redirect('/branch-home')
    


@login_required(login_url='/login/')
def add_employee(Request):
    if Branch.objects.filter(email=Request.user.username):
    
       uname=User.objects.all()
       if(Request.method=="POST"):
           b=Employee()
           b.name=Request.POST.get('name')
           b.email=Request.POST.get('email')
           b.password=Request.POST.get('password')
           b.address=Request.POST.get('address')
           try:
                u=Employee.objects.get(username=b.email)
                if(u):
                   pass
           except:
                   user = User(username=b.email, email=b.email,first_name=b.name)
                   if (user):
                       user.set_password(b.password)
                       user.save()
                       b.save()
                       return redirect('/employee')
       return render(Request,'branch/add-employee.html',{'uname':uname})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")

@login_required(login_url='/login/')
def employee_page(Request):
    if Branch.objects.filter(email=Request.user.username):
    
       data=Employee.objects.all().order_by('id').reverse()
       return render(Request,'branch/employee.html',{'data':data})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")

@login_required(login_url='/login/')
def update_employee(Request,id):
    if Branch.objects.filter(email=Request.user.username):
       data=Employee.objects.get(id=id)
       if(Request.method=="POST"):
           data.name=Request.POST.get('name')
           data.address=Request.POST.get('address')
           data.save()
           return redirect('/employee')
       return render(Request,'branch/update-employee.html',{'data':data})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")


@login_required(login_url='/login/')
def delete_employee(Request,id):
    if Branch.objects.filter(email=Request.user.username):
       data=Employee.objects.get(id=id)
       u=User.objects.get(username=data.email)
       if(u):
         u.delete()
       data.delete()
       return redirect('/employee')
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")



@login_required(login_url='/login/')
def employee_home(Request):
    if Employee.objects.filter(email=Request.user.username):
    
        tt = Decimal(0)
        shift_totals = {'1': Decimal(0), '2': Decimal(0), '3': Decimal(0)}
        
        data = Receipt.objects.all().order_by('id').reverse()
        current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_datetime_ist = current_datetime_utc.astimezone(indian_timezone)
        formatted_date = current_datetime_ist.strftime("%d/%b/%Y")
        
        t = Receipt.objects.filter(date__startswith=formatted_date,employee_email=Request.user.username)
        
        for i in t:
            tt += Decimal(i.amount)
            shift_totals[i.shift_name] = shift_totals.get(i.shift_name, Decimal(0)) + Decimal(i.amount)
        
        # Now shift_totals contains the total amount for each shift, even if the shift name is not present in the Receipt objects
        s1 = shift_totals.get('01', Decimal(0))
        s2 = shift_totals.get('02', Decimal(0))
        s3 = shift_totals.get('03', Decimal(0))
        return render(Request,'employee/employee-index.html',{'data':t,'tt':tt,'s1':s1,'s2':s2,'s3':s3})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")


@login_required(login_url='/login/')
def employee_total_receipt(Request):
    if Employee.objects.filter(email=Request.user.username):
    
      tt = Decimal(0)
      shift_totals = {'1': Decimal(0), '2': Decimal(0), '3': Decimal(0)}
      if Request.method == "POST":
         from_date_str = Request.POST.get('from_date')
         to_date_str = Request.POST.get('to_date')
         
         # Convert string dates to datetime objects
         from_date = datetime.strptime(from_date_str, '%Y-%m-%d').replace(tzinfo=pytz.timezone('Asia/Kolkata'))
         to_date = datetime.strptime(to_date_str, '%Y-%m-%d').replace(tzinfo=pytz.timezone('Asia/Kolkata'))
         
         # Print only the date part
         from_date_tl = from_date.strftime('%d/%b/%Y %I:%M %p')
         to_date_tl = to_date.strftime('%d/%b/%Y %I:%M %p')
         
         print("From Date:", from_date_tl, "To Date:", to_date_tl)
         
         # Filter data between from_date and to_date (inclusive)
         data = Receipt.objects.filter(date__range=[from_date_tl, to_date_tl],employee_email=Request.user.username).order_by('id').reverse()
     
         # ... rest of your code ...
         if data:
             print("Hi")
     
         for i in data:
             tt += Decimal(i.amount)
             shift_totals[i.shift_name] = shift_totals.get(i.shift_name, Decimal(0)) + Decimal(i.amount)
    
         # Now shift_totals contains the total amount for each shift within the specified date range
         s1 = shift_totals.get('01', Decimal(0))
         s2 = shift_totals.get('02', Decimal(0))
         s3 = shift_totals.get('03', Decimal(0))
        
            
      else:
        tt = Decimal(0)
        shift_totals = {'1': Decimal(0), '2': Decimal(0), '3': Decimal(0)}
        
        data = Receipt.objects.filter(employee_email=Request.user.username).order_by('id').reverse()
        current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_datetime_ist = current_datetime_utc.astimezone(indian_timezone)
        formatted_date = current_datetime_ist.strftime("%d/%b/%Y")
        
        t = Receipt.objects.filter(employee_email=Request.user.username)
        
        for i in t:
            tt += Decimal(i.amount)
            shift_totals[i.shift_name] = shift_totals.get(i.shift_name, Decimal(0)) + Decimal(i.amount)
        
        # Now shift_totals contains the total amount for each shift, even if the shift name is not present in the Receipt objects
        s1 = shift_totals.get('01', Decimal(0))
        s2 = shift_totals.get('02', Decimal(0))
        s3 = shift_totals.get('03', Decimal(0))
      return render(Request,'employee/total-receipt.html',{'data':data,'tt':tt,'s1':s1,'s2':s2,'s3':s3})
    else:
        return HttpResponseForbidden("You don't have permission to access this page.")



@login_required(login_url='/login/')
def add_employee_receipt(Request):
 if Employee.objects.filter(email=Request.user.username):
    
        vehicle=Vehicle.objects.all()
        if Request.method=="POST":
            r=Receipt()
            current_datetime_utc = datetime.utcnow().replace(tzinfo=pytz.utc)

            # Convert UTC time to Indian Standard Time (IST)
            indian_timezone = pytz.timezone('Asia/Kolkata')
            current_datetime_ist = current_datetime_utc.astimezone(indian_timezone)
            
            # Format the date and time as required in IST
            formatted_datetime = current_datetime_ist.strftime("%d/%b/%Y %I:%M %p")
            
            # Create a Receipt instance
            r = Receipt()
            r.date = formatted_datetime
            r.operator_class = Request.POST.get('operator_class')
            r.vehicle_number = Request.POST.get('vehicle_number')
            r.employee_email=Request.user.username
            
            # Define shift timings
            shift_timings = {
                '01': (datetime.strptime('00:00', '%H:%M'), datetime.strptime('07:59', '%H:%M')),
                '02': (datetime.strptime('08:00', '%H:%M'), datetime.strptime('15:59', '%H:%M')),
                '03': (datetime.strptime('16:00', '%H:%M'), datetime.strptime('23:59', '%H:%M'))
            }
            
            # Determine the shift based on current time
            current_time = current_datetime_ist.time()
            for shift_name, (start_time, end_time) in shift_timings.items():
                start_time = start_time.time()
                end_time = end_time.time()
                if start_time <= current_time <= end_time:
                    r.shift_name = shift_name
                    break
            else:
                # Handle the case where the current time does not fall into any shift
                r.shift_name = 'Unknown'
            
            # Use r.shift_name as needed
            try:
                v=Vehicle.objects.get(name=r.operator_class)
                r.amount=v.price
            except:
                pass
            
            r.save()
            hm=int(r.amount/2)
    
    
            return render(Request,'receipt.html',{'data':r,'hm':hm})


        return render(Request,'employee/add-receipt.html',{'vehicle':vehicle})
 else:
     return HttpResponseForbidden("You don't have permission to access this page.")

