from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('items', views.items, name='client-items'),
    path('order', views.order, name='client-order'),
    path('dashboard', views.dashboard, name='client-dashboard'),
    path('logout', views.logout, name='logout'),
]