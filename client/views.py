from django.db import connection
from django.shortcuts import render
# Create your views here.


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def store(request):
    """Displays a table that contains all items"""
    cursor = connection.cursor()
    query = "SELECT * FROM item"

    # filter results
    if 'filter' in request.GET:
        param_filter = request.GET.get('filter')
        if param_filter == "AVAILABLE":
            query += " WHERE quantity > 0"

    # order results
    if 'sort' in request.GET:
        sort = request.GET.get('sort')
        # sort by quantity
        if sort == 'QUANTITY_DESC':
            query += ' ORDER BY quantity DESC'
        elif sort == 'QUANTITY_ASC':
            query += ' ORDER BY quantity ASC'

        # sort by name
        elif sort == "NAME_ASC":
            query += ' ORDER BY name ASC'
        elif sort == "NAME_DESC":
            query += " ORDER BY name DESC"

        # sort by id
        elif sort == "ID_ASC":
            query += " ORDER BY item_id ASC"
        elif sort == "ID_DESC":
            query += " ORDER BY item_id DESC"

        # sort by price
        elif sort == "PRICE_ASC":
            query += " ORDER BY price ASC"
        elif sort == "PRICE_DESC":
            query += " ORDER BY price DESC"

    cursor.execute(query + ";")

    context = {'items': dictfetchall(cursor)}

    return render(request, "client/store.html", context)
