from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from client import forms
from client.helper_funcs import dictfetchall
from datetime import date

# Create your views here.


def items(request):
    """Displays a table that contains all items"""
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

    return render(request, "client/items.html", context)


@login_required
def order(request):
    """Form where a customer can order an item"""
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

                        # Update quantity of item
                        cursor.execute(
                            "UPDATE item SET quantity = {} WHERE item_id = {};".format(item["quantity"] - quantity, item_id))

                        return HttpResponseRedirect("/client/items")
    else:
        # blank form if GET request
        form = forms.OrderForm()

    context = {
        'form': form,
    }
    return render(request, 'client/order.html', context)
