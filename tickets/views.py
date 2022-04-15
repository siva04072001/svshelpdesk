from multiprocessing import context
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

import tickets
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from .models import *
from django.contrib import messages
import datetime
from django.core.paginator import Paginator
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
# Create your views here.

#home page
def index(request):
    return render(request, 'index.html')



#register new user
def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            userId = form.cleaned_data.get('userId')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            msg = 'user created'
            send_mail(
                'SVS Help Desk Registered sucessfully',
                f'hi {username}:\n'+
                f'\nWelcome to Our Help Desk Services\n'+
                f'\nUser Name: {username}\n'+
                f'\npassword: {password}\n'+
                f'\nregistration sucessfull...\n',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request,'Registered Sucessfully.....')
            return redirect('register')
            
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})
    

#login user
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superadmin:
                login(request, user)
                return redirect('superadmin')
            elif user is not None and user.is_admin:
                login(request, user)
                return redirect('admin')
            elif user is not None and user.is_engineer:
                login(request, user)
                return redirect('engineer')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

#logout user
def logout_view(request):
    logout(request)
    return redirect('/login')

#enter superadmin after login
@login_required(login_url='login')
def superadmin(request):
    if request.user.is_authenticated:
        return render(request,'superadmin.html')
    else:
        return render(request, 'login.html', {}) 

#super admin user view page
@login_required(login_url='login')
def superadminview(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            user=User.objects.all()
            p=Paginator(User.objects.all(), 10)
            page=request.GET.get('page')
            users=p.get_page(page)
        return render(request, 'superadminview.html',{"user": user, "users":users})

    else:
        return render(request, 'login.html', {})

#admin page after login
@login_required(login_url='login')
def admin(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            tickets=Tickets.objects.all()
            
        return render(request, 'admin.html',{"tickets":tickets})

    else:
        return render(request, 'login.html', {})

#closed ticket section in admin page
@login_required(login_url='login')
def adminclosed(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            ticket=Tickets.objects.all()
            p=Paginator(Tickets.objects.all(), 10)
            page=request.GET.get('page')
            tickets=p.get_page(page)
        return render(request, 'adminclosed.html',{"ticket": ticket, "tickets":tickets})

    else:
        return render(request, 'login.html', {})

#engineer page after login
@login_required(login_url='login')
def engineer(request):
    if request.user.is_authenticated:
        return render(request,'engineer.html')
    else:
        return render(request, 'login.html', {}) 

#employee page after login
@login_required(login_url='login')
def employee(request):
    if request.user.is_authenticated:
        ticket=User.objects.all()
        return render(request,'employee.html' ,{"ticket": ticket})
        
    else:
        return render(request, 'login.html', {}) 

#employee status page
@login_required(login_url='login')
def statusticket(request):
    if request.user.is_authenticated:
        ticket=Tickets.objects.filter(username=request.user)
        return render(request, 'employee_status.html',{"ticket": ticket})

    else:
        return render(request, 'login.html', {}) 

#engineer status page
@login_required(login_url='login')
def engineerticket(request):
    if request.user.is_authenticated:
        
        
        ticket=Tickets.objects.filter(assigned=request.user)
        return render(request, 'engineer.html', {"ticket": ticket})

    else:
        return render(request, 'login.html', {}) 

#engineer ticket closed page
@login_required(login_url='login')
def engineerticketclosed(request):
    if request.user.is_authenticated:
        
        
        ticket=Tickets.objects.filter(assigned=request.user)
        return render(request, 'engineerclosed.html', {"ticket": ticket})

    else:
        return render(request, 'login.html', {})

#admin closed ticket page
@login_required(login_url='login')
def close_ticket(request,Id):
    tickets=Tickets.objects.all()
    item=Tickets.objects.get(Id=Id)
    item.status="closed"
    item.save()
    context={
        'item':item,
        'tickets':tickets   
    }
    messages.info(request,"Ticket Updated")
    return render(request, 'admin.html', context)

#admin edit page
@login_required(login_url='login')
def assign_ticket(request,Id):
    eng=User.objects.all()
    item=Tickets.objects.get(Id=Id)
    item_list=Tickets.objects.all()
    context={
        'item':item,
        'item_list':item_list,
        'eng':eng
    }
    return render(request, 'adminedit.html', context)

#super admin edit user page
@login_required(login_url='login')
def assign_user(request,Id):
    item=User.objects.get(userId = Id)
    context={
        'item':item
    }
    return render(request, 'superadminedit.html', context)

#super admin update user process
@login_required(login_url='login')
def update_user(request,Id):
    
    item=User.objects.get(userId=Id)
    email=request.POST['email']
    mobNo=request.POST['mobNo']
    address=request.POST['address']
    designation=request.POST['designation']
    is_admin=request.POST['is_admin']
    is_engineer=request.POST['is_engineer']
    is_employee=request.POST['is_employee']
    reg =User(email=email,mobNo=mobNo,address=address,designation=designation,
    is_admin=is_admin,is_engineer=is_engineer,is_employee=is_employee)
    reg.save()
    context={
        'item':item,
        
        
    }
    messages.info(request,"Ticket Updated")
    return render(request, 'superadminedit.html', context)

#super admin delete user 
@login_required(login_url='login')
def delete_user(request,Id):
    
    item=User.objects.get(userId=Id)
    
    item.delete()
    
    messages.info(request,"user deleted")
    user=User.objects.all()
    p=Paginator(User.objects.all(), 10)
    page=request.GET.get('page')
    users=p.get_page(page)
    return render(request, 'superadminview.html',{"user": user, "users":users})

#superadmin update user process
@login_required(login_url='login')
def update_user(request,Id):
    
    item=User.objects.get(userId=Id)
    item.email=request.POST['email']
    item.mobNo=request.POST['mobNo']
    item.address=request.POST['address']
    item.designation=request.POST['designation']
    item.save()
    context={
        'item':item
        
    }
    messages.info(request,"User Updated")
    return render(request, 'superadminedit.html', context)

#admin update ticket process
@login_required(login_url='login')
def update_ticket(request,Id):
    eng=User.objects.all()
    item=Tickets.objects.get(Id=Id)
    item.due_date=request.POST['due_date']
    item.assigned=request.POST['assigned']
    item.status="assigned"
    item.save()
    context={
        'item':item,
        'eng':eng
        
    }
    messages.info(request,"Ticket Assigned")
    return render(request, 'adminedit.html', context)

#engineer status page
@login_required(login_url='login')
def engassign_ticket(request,Id):
    eng=User.objects.all()
    item=Tickets.objects.get(Id=Id)
    item_list=Tickets.objects.all()
    context={
        'item':item,
        'item_list':item_list,
        'eng':eng
    }
    return render(request, 'engineer_status.html', context)

#engineer update process
@login_required(login_url='login')
def engupdate_ticket(request,Id):
    item=Tickets.objects.get(Id=Id)
    item.status=request.POST['status']
    item.save()
    eng=User.objects.get(username=item.assigned)
    context={
        'item':item,
        'eng':eng
        
    }
    messages.info(request,"Ticket Updated")
    return render(request, 'engineer_status.html', context)

#new ticket user page
@login_required(login_url='login')
def userticket(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            
            username=request.user
            category=request.POST["category"]
            location=request.POST["location"]
            subfactory=request.POST["subfactory"]
            item=request.POST["item"]
            queries=request.POST["queries"]
            Description=request.POST["Description"]
            mobileNo=request.POST["mobileNo"]
            mail=request.user.email
            priority=request.POST["priority"]
            uploadFile=request.FILES['file']
            status="not assigned"
            assigned="not assigned"
            assigned_date=datetime.date.today()
            if item == 'others':
                activateitem='True'
                item=request.POST['itemothers']
        
        
            ticket= Tickets(username=username,category=category,location=location,subfactory=subfactory,item=item,
            queries=queries,Description=Description,mobileNo=mobileNo,mail=mail,priority=priority,status=status,
            assigned=assigned,assigned_date=assigned_date,uploadFile=uploadFile)
            ticket.save()
            messages.success(request,'Ticket Generated Sucessfully.....')
        
        
        return render(request, 'employee.html', {})
    else:
        return render(request, 'login.html', {}) 