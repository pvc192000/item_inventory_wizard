from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.models import User, auth 
# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def dashboard(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM staff WHERE email = '%s';" %str(request.user.email))

    context = {'info': dictfetchall(cursor)}
    return render(request,'staff_dashboard.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')

def items(request):
    """Displays a table that contains all items"""

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM item ORDER BY item.quantity asc;")

    context = {'items': dictfetchall(cursor)}
    
    return render(request, 'items_staff.html', context)

def item_orders(request):

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM order_from ORDER BY quantity asc;")

    context = {'item_orders': dictfetchall(cursor)}
    
    return render(request, 'item_orders.html', context)


def delivered(request):
    
    return render(request, 'delivered_items.html')

def help(request):
    
    return render(request, 'help.html')
