from django.contrib import admin
from django.urls import path, include
from client import views


urlpatterns = [
    path('items', views.items, name='client-items'),
]
