from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from customer import forms
from customer.helper_funcs import dictfetchall
from datetime import date
from django.contrib.auth.models import User, auth

# Create your views here.


@login_required
def items(request):
    """Displays a table that contains all items"""
    if request.user.is_staff or request.user.is_superuser:
        raise PermissionDenied
    cursor = connection.cursor()
    query = "SELECT * FROM item"
    sortAsc = False
    # filter results
    if 'filter' in request.GET:
        param_filter = request.GET.get('filter')
        if param_filter == "AVAILABLE":
            query += " WHERE quantity > 0"

    # order results
    if 'sort' in request.GET:
        sort = request.GET.get('sort')
        # sort by quantity
        if sort == 'QUANTITY_ASC':
            query += ' ORDER BY quantity ASC'
            sortAsc = True
        elif sort == 'QUANTITY_DESC':
            query += ' ORDER BY quantity DESC'
            sortAsc = False

        # sort by name
        elif sort == "NAME_ASC":
            query += ' ORDER BY name ASC'
            sortAsc = True
        elif sort == "NAME_DESC":
            query += " ORDER BY name DESC"
            sortAsc = False

        # sort by id
        elif sort == "ID_ASC":
            query += " ORDER BY item_id ASC"
            sortAsc = True
        elif sort == "ID_DESC":
            query += " ORDER BY item_id DESC"
            sortAsc = False

        # sort by price
        elif sort == "PRICE_ASC":
            query += " ORDER BY price ASC"
            sortAsc = True
        elif sort == "PRICE_DESC":
            query += " ORDER BY price DESC"
            sortAsc = False

    cursor.execute(query + ";")

    context = {
        'items': dictfetchall(cursor),
        'sortAsc': sortAsc
    }

    return render(request, "customerItems.html", context)


@login_required
def order(request):
    """Form where a customer can order an item"""
    if request.user.is_staff or request.user.is_superuser:
        raise PermissionDenied
    # fetch items from db
    cursor = connection.cursor()
    query = "SELECT item_id, quantity FROM item"
    cursor.execute(query + ";")
    items = dictfetchall(cursor)

    if request.method == 'POST':
        form = forms.OrderForm(request.POST)

        if form.is_valid():
            # validate data:
            item_id = form.cleaned_data["item_id"]
            quantity = form.cleaned_data["quantity"]
            # make changes to database
            for item in items:
                if item["item_id"] == item_id:
                    if item["quantity"] - quantity >= 0:
                        # obtain user id
                        cursor.execute("SELECT customer_id FROM customer WHERE email = '{}';".format(
                            request.user.email))
                        customer_id = dictfetchall(cursor)[0]["customer_id"]

                        # create new purchase row
                        today = date.today().strftime("%Y-%m-%d")
                        cursor.execute("INSERT INTO purchase (purchase_date, item_id, quantity, customer_id) VALUES ('{}', {}, {}, {});".format(
                            today, item_id, quantity, customer_id))

                        return HttpResponseRedirect("/customer/order")
    else:
        # blank form if GET request
        form = forms.OrderForm()
    """Table that shows all purchases made by customer"""
    cursor = connection.cursor()
    # obtain user id
    cursor.execute("SELECT customer_id FROM customer WHERE email = '{}';".format(
        request.user.email))
    customer_id = dictfetchall(cursor)[0]["customer_id"]

    # get all purchases from customer
    query = "SELECT P.purchase_date, P.quantity, P.item_id, I.price, I.name FROM purchase P, item I WHERE P.customer_id={} AND P.item_id=I.item_id ORDER BY P.purchase_date DESC".format(
        customer_id)
    cursor.execute(query + ";")

    context = {"items": dictfetchall(cursor), 'form': form, }
    return render(request, 'customerOrder.html', context)


@login_required
def dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        raise PermissionDenied
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM customer WHERE email = '%s';" %
                   str(request.user.email))

    context = {'info': dictfetchall(cursor)}
    return render(request, 'customerDashboard.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')
