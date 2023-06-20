from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
# from ..products.models import *
from products.models import Customer

# if __name__ == "__pyshop-Deploy__" and __package__ is None:
#     from sys import path
#     from os.path import dirname as dir

#     path.append(dir(path[0]))
#     __package__ = "products"
#     import models


def home(request):
    if request.user.is_authenticated:
        fname = request.user.get_short_name()
        signin_btn_txt = "Hello, {}".format(fname)
        return render(request, 'index2.html', {'signin_btn_txt': signin_btn_txt})
    else:
        if request.method == "POST":
            username = request.POST['username']
            pass1 = request.POST['pass1']
            
            user = authenticate(username=username, password=pass1)
            
            context = {}
            context.update(csrf(request))
            
            if user is not None:
                login(request, user)
                # username = username
                fname = user.first_name
                return render(request, 'index2.html', {"fname": fname})
            
            else:
                messages.error(request, "Bad credentials")
                return redirect('/auth') # ('register/') IMP
        
        signin_btn_txt = "Hello, Sign-In"        
        return render(request, 'home.html', {'signin_btn_txt': signin_btn_txt})



def register(request):
    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        email = request.POST['email']
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist!")
            return redirect('/auth/register')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('/auth/register')
        
        if len(phone)!=10:
            messages.error(request, "Please enter correct Mobile number")
            return redirect('/auth/register')
            
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('/auth/register')
        
        if len(pass1)<6:
            messages.error(request, "Password must be atleast 6 characters")
            return redirect('/auth/register')

        if pass1!=pass2:
            messages.error(request, "Passwords didn't match!")
            return redirect('/auth/register')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.phone = phone
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        
        # Creating a new customer with the registered user :-
        mycustomer = Customer(user = myuser,
                              name = myuser.username,
                              email = myuser.email)
        mycustomer.save()
        
        # Logging-In the new user :-
        login(request, myuser)
        
        messages.success(request, "Account created successfully.")
        
        context = {}
        context.update(csrf(request))
        
        return redirect('/auth/')
        
    signin_btn_txt = "Hello, Sign-In"
    return render(request, 'register.html', {'signin_btn_txt': signin_btn_txt})


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('/')