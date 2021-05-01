from django.shortcuts import render

# Create your views here.
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


def dashboard(request):
    if not request.user.is_staff:
        raise PermissionDenied
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM staff WHERE email = '%s';" %
                   str(request.user.email))

    context = {'info': dictfetchall(cursor)}
    return render(request, 'staff_dashboard.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/')


def items(request):
    if not request.user.is_staff:
        raise PermissionDenied
    """Displays a table that contains all items"""

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM item ORDER BY item.quantity asc;")

    context = {'items': dictfetchall(cursor)}

    return render(request, 'items_staff.html', context)


def item_orders(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == "POST":
        c_id = int(request.POST['customer_id'])
        i_id = int(request.POST['item_id'])
        qty = int(request.POST['quantity'])
        cursor = connection.cursor()
        cursor.execute(
            "SELECT quantity FROM item where item_id = {};" .format(i_id))
        items = dictfetchall(cursor)
        original_qty = 0
        original_qty = items[0]['quantity']
        cursor.execute("UPDATE item SET quantity = {} WHERE item_id = {};".format(
            original_qty - qty, i_id))
        cursor = connection.cursor()
        cursor.execute(
            "Delete FROM purchase where customer_id = {} and item_id = {} and quantity = {}" .format(c_id, i_id, qty))
        cursor = connection.cursor()
        cursor.execute("SELECT p.purchase_date, p.quantity, p.customer_id, c.name as cname, p.item_id, i.name as iname FROM purchase as p, customer as c, item as i WHERE p.customer_id = c.customer_id AND p.item_id = i.item_id ORDER BY p.purchase_date asc;")

        context = {'items_orders': dictfetchall(cursor)}
        return render(request, 'item_orders.html', context)
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT p.purchase_date, p.quantity, p.customer_id, c.name as cname, p.item_id, i.name as iname FROM purchase as p, customer as c, item as i WHERE p.customer_id = c.customer_id AND p.item_id = i.item_id ORDER BY p.purchase_date asc;")

        context = {'item_orders': dictfetchall(cursor)}

        return render(request, 'item_orders.html', context)


def delivered(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == "POST":
        o_id = int(request.POST['order_id'])
        i_id = int(request.POST['item_id'])
        qty = int(request.POST['quantity'])
        cursor = connection.cursor()
        cursor.execute(
            "SELECT quantity FROM item where item_id = {};" .format(i_id))
        items = dictfetchall(cursor)
        original_qty = 0
        for item in items:
            original_qty = item['quantity']
        cursor.execute("UPDATE item SET quantity = {} WHERE item_id = {};".format(
            original_qty + qty, i_id))
        cursor = connection.cursor()
        cursor.execute(
            "Delete FROM order_from where order_id = {}" .format(o_id))
        cursor = connection.cursor()
        cursor.execute("select o.order_id, o.quantity, o.item_id, i.name  from order_from as o, supplier as s, item as i where o.item_id = i.item_id AND o.supplier_id = s.supplier_id and (o.order_date + s.avg_delivery_time) < now();")

        context = {'items': dictfetchall(cursor)}
        return render(request, 'delivered_items.html', context)
    else:
        cursor = connection.cursor()
        cursor.execute("select o.order_id, o.quantity, o.item_id, i.name  from order_from as o, supplier as s, item as i where o.item_id = i.item_id AND o.supplier_id = s.supplier_id and (o.order_date + s.avg_delivery_time) < now();")

        context = {'items': dictfetchall(cursor)}

        return render(request, 'delivered_items.html', context)


def help(request):

    return render(request, 'help.html')
