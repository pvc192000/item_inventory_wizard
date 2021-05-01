from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.models import User, auth
from django.core.exceptions import PermissionDenied
# Create your views here.


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def items(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM item ORDER BY item.quantity asc;")

    context = {'items': dictfetchall(cursor)}
    return render(request, 'items.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/')


def suppliers(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        i_id = int(request.POST['item_id'])
        cursor = connection.cursor()
        cursor.execute("SELECT s.supplier_id, s.avg_delivery_time, s.name, s.email, s.phone, i.item_id, i.name as i_name FROM supplier as s, supplied_by as b, item as i WHERE s.supplier_id = b.supplier_id AND b.item_id = i.item_id AND b.item_id = %d " % i_id)

        context = {'suppliers': dictfetchall(cursor)}
        return render(request, 'suppliers.html', context)
    else:
        return render(request, 'suppliers.html')


def sorders(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        m_id = int(request.POST['manager_id'])
        s_id = int(request.POST['supplier_id'])
        i_id = int(request.POST['item_id'])
        qty = int(request.POST['quantity'])
        cursor = connection.cursor()
        cursor.execute("INSERT INTO order_from (manager_id, supplier_id, quantity, item_id, order_date) VALUES (%d, %d, %d, %d, now()); " % (
            m_id, s_id, qty, i_id))
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM order_from ORDER BY order_date desc")

        context = {'sorders': dictfetchall(cursor)}
        return render(request, 'sorders.html', context)
    else:

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM order_from ORDER BY order_date desc")

        context = {'sorders': dictfetchall(cursor)}
        return render(request, 'sorders.html', context)


def dashboard(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM manager WHERE email = '%s';" %
                   str(request.user.email))

    context = {'info': dictfetchall(cursor)}
    return render(request, 'dashboard.html', context)
