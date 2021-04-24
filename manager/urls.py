from django.urls import path

from . import views

urlpatterns = [
    path('items', views.items, name='items'),
    path('logout', views.logout, name='logout'),
    path('suppliers', views.suppliers, name='suppliers'),
    path('sorders', views.sorders, name='sorders'),
    path('dashboard', views.dashboard, name='dashboard'),
]
