from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *

import bcrypt

# Create your views here.
def index(request):
    return render(request,'main/index.html')

def register(request):
    form = request.POST

    errors = User.objects.basic_validator(form)

    if len(errors)>0:
        for key, val in errors.items():
            messages.error(request,val)
        return redirect('/')
    
    user = User.objects.create(
        first_name= form["first_name"],
        last_name= form["last_name"],
        email= form["email"],
        password = bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt()),
        birthday = form["birthday"],
    )
    request.session["user_id"] = user.id

    return redirect('/success')

def login(request):
    form = request.POST
    # print(form)
    try:
        user=User.objects.get(email=form["login_email"])
    except:
        messages.error(request,"Please enter a correct email!")
        return redirect("/")
    if bcrypt.checkpw(form["login_password"].encode(), user.password.encode()) == False:
        messages.error(request,"Please enter a correct password!")
        return redirect("/")
    
    request.session["user_id"] = user.id
    return redirect("/success")

def success(request):
    user = User.objects.get(id=request.session['user_id'])

    return render(request,'main/success.html',{
        "user": user,
    })

def logout(request):
    request.session.clear
    return redirect('/')