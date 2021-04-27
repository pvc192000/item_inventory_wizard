from django.urls import path

from . import views

urlpatterns = [
    path('items_staff', views.items, name='items'),
    path('logout', views.logout, name='logout'),
    path('item_orders', views.item_orders, name='item_orders'),
    path('staff_dashboard', views.dashboard, name='dashboard'),
    path('delivered_items', views.delivered, name="delivered_items"),
    path('help', views.help, name="help"),
]
