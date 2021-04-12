from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth 

# Create your views here.

def login(request):
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        first_name = request.POST['exampleFirstName']
        last_name = request.POST['exampleLastName']
        user_name = request.POST['exampleUserName']
        email = request.POST['exampleInputEmail']
        password1 = request.POST['exampleInputPassword']
        password2 = request.POST['exampleRepeatPassword']

        if password1 == password2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=user_name, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request,'user created')
                print('user created')
                return redirect('/')        
        else:
            messages.info(request,'password not matching')
            return redirect('register')
        return redirect('/') # change this to home page
    return render(request, 'register.html')