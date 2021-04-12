from django.shortcuts import render
from django.db import connection

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
    cursor.execute("SELECT * FROM client_item WHERE quantity > 0;")

    context = {'items': dictfetchall(cursor)}

    return render(request, "client/store.html", context)
