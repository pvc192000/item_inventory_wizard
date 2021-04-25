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
