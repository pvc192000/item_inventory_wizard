from django.db import models

# Create your models here.


class Item(models.Model):
    """Represents an item the store sells"""
    quantity = models.IntegerField()
    price = models.FloatField()
    name = models.CharField(max_length=200)
    item_id = models.IntegerField(primary_key=True)
    available_by = models.DateField()
