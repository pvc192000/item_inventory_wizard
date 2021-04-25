from django import forms


class OrderForm(forms.Form):
    item_id = forms.IntegerField()
    quantity = forms.IntegerField()
