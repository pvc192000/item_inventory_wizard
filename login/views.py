from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth 
from django.db import connection

# Create your views here.

def login(request):
    if request.method=="POST":
        username = request.POST['exampleUserName']
        password = request.POST['exampleInputPassword']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_superuser == True:
                return redirect("manager/dashboard")
            elif user.is_staff == True:
                return redirect("staff/dashboard")
            else:
                return redirect("customer/dashboard")
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        first_name = request.POST['exampleFirstName']
        last_name = request.POST['exampleLastName']
        user_name = request.POST['exampleUserName']
        email = request.POST['exampleInputEmail']
        password1 = request.POST['exampleInputPassword']
        password2 = request.POST['exampleRepeatPassword']
        phone = request.POST['phone']
        role = request.POST['role']

        if password1 == password2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('register')
            elif role != 'manager' and role != 'staff' and role != 'customer':
                messages.info(request, 'incorrect role select from customer/manager/staff')
                return redirect('register')
            else:
                user = User.objects.create_user(username=user_name, password=password1, email=email, first_name=first_name, last_name=last_name)
                cursor = connection.cursor()
                if role == 'manager':
                    user.is_superuser = True
                    cursor.execute("INSERT INTO manager (name, phone, email) VALUES ('" + str(first_name) + " " + str(last_name) + "', '" + str(phone) + "', '" + str(email) + "');")
                    user.save()
                    messages.info(request,'user created') 
                    return redirect('/')
                elif role == 'staff':
                    user.is_staff = True
                    cursor.execute("INSERT INTO staff (name, phone, email) VALUES ('" + str(first_name) + " " + str(last_name)+ "', '" + str(phone) + "', '" + str(email) + "');")
                    user.save()
                    messages.info(request,'user created') 
                    return redirect('/')
                else:
                    cursor.execute("INSERT INTO customer (name, phone, email) VALUES ('" + str(first_name) + " " + str(last_name)+ "', '" + str(phone) + "', '" + str(email) + "');")
                    user.save()
                    messages.info(request,'user created') 
                    return redirect('/')           
        else:
            messages.info(request,'password not matching')
            return redirect('register')
        return redirect('/') # change this to home page
    return render(request, 'register.html')


