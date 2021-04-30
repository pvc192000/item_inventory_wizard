from django.urls import path

from . import views

urlpatterns = [
    path('items', views.items, name='items'),
    path('logout', views.logout, name='logout'),
    path('orders', views.item_orders, name='item_orders'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('delivered_items', views.delivered, name="delivered_items"),
    path('help', views.help, name="help"),
]
