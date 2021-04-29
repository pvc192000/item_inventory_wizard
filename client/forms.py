from django import forms
from django.core.exceptions import ValidationError
from django.db import connection
from client.helper_funcs import dictfetchall


class OrderForm(forms.Form):
    item_id = forms.IntegerField(required=True)
    quantity = forms.IntegerField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        item_id = cleaned_data.get("item_id")
        quantity = cleaned_data.get("quantity")

        if item_id and quantity:
            cursor = connection.cursor()
            query = "SELECT item_id, quantity FROM item"
            cursor.execute(query + ";")
            items = dictfetchall(cursor)
            id_exists = False
            for item in items:
                if item["item_id"] == item_id:
                    id_exists = True
                    if item["quantity"] - quantity < 0:
                        raise ValidationError("Not enough units in stock.")

            if not id_exists:
                raise ValidationError("Id does not exist")
