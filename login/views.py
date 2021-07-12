from Administrator.views import dictfetchall
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth 
from django.db import connection

# Implemention file for the Login Model of the CPMS website. View function for each url call in the Login model is found here.

# Logs in a user and directs to a particular view of the website based on their role : Admin/Author/Reviewer
def login(request):
    if request.method=="POST":
        username = request.POST['exampleUserName']
        password = request.POST['exampleInputPassword']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_superuser == True:
                return redirect("administrator/matchPaperWithReviewers")
            elif user.is_staff == True:
                return redirect("reviewer/reviewerRegisterToReviewPapers")
            else:
                return redirect("author/authorRegisterToSubmitPaper")
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

# Registers a new Author/Reviewer into the website. Creates a new Django User and Author/Reviewer in the backend (CPMS database)
def register(request):
    if request.method == "POST":
        first_name = request.POST['exampleFirstName']
        last_name = request.POST['exampleLastName']
        user_name = str(request.POST['exampleInputEmail'])
        middle_initial = request.POST['exampleMiddleInitial']
        password1 = request.POST['exampleInputPassword']
        password2 = request.POST['exampleRepeatPassword']
        role = request.POST['role']
        print(role)

        if password1 == password2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=user_name, password=password1, email=user_name, first_name=first_name, last_name=last_name)
                cursor = connection.cursor()
                if role == 'authorRole':
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO dbo.Author (FirstName, LastName, MiddleInitial, Password, EmailAddress) VALUES ('{}', '{}', '{}', '{}', '{}')".format(first_name,last_name,middle_initial,password1,user_name))
                    user.save()
                    messages.info(request,'user created') 
                    return redirect('/')
                elif role == 'reviewerRole':
                    user.is_staff = True
                    cursor.execute("INSERT INTO dbo.Reviewer (FirstName, LastName, MiddleInitial, Password, EmailAddress) VALUES ('{}', '{}', '{}', '{}', '{}')".format(first_name,last_name,middle_initial,password1,user_name))
                    user.save()
                    messages.info(request,'user created') 
                    return redirect('/')          
        else:
            messages.info(request,'password not matching')
            return redirect('register')
        return redirect('/') 
    return render(request, 'register.html')

# Gives the user an option to change password, if the user gives other correct credentials
def forgotPassword(request):
    if request.method == 'POST':
        first_name = request.POST['exampleFirstName']
        last_name = request.POST['exampleLastName']
        user_name = str(request.POST['exampleInputEmail'])
        password1 = request.POST['exampleInputPassword1']
        password2 = request.POST['exampleInputPassword2']
        role = request.POST['role']

        if password1 == password2:
            if User.objects.filter(username=user_name).exists():
                cursor = connection.cursor()
                if role == 'Author':
                    cursor.execute("SELECT Password FROM dbo.Author WHERE EmailAddress = '{}'".format(user_name))
                    password = (dictfetchall(cursor))[0]['Password']
                    user = auth.authenticate(username = user_name, password = password , first_name = first_name, last_name = last_name)
                elif role == 'Reviewer':
                    cursor.execute("SELECT Password FROM dbo.Reviewer WHERE EmailAddress = '{}'".format(user_name))
                    password = (dictfetchall(cursor))[0]['Password']
                    user = auth.authenticate(username = user_name, password = password, first_name = first_name, last_name = last_name)
                
                if user is not None:
                    user.set_password(password1)
                    user.save()
                    cursor = connection.cursor()
                    if role == 'Author':
                        cursor.execute("Update dbo.Author SET Password = '{}' WHERE EmailAddress = '{}'".format(password1, user_name))
                    elif role == 'Reviewer':
                        cursor.execute("Update dbo.Reviewer SET Password = '{}' WHERE EmailAddress = '{}'".format(password1, user_name))
                    messages.info(request, 'Password changed')
                    return redirect('login')
                else:
                    messages.info(request, 'Invalid Credentials')
                    return redirect('forgotPassword')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('forgotPassword')
    else:
        return render(request, 'forgotPassword.html')