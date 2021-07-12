from django.contrib import admin
from django.urls import path, include
from . import views

# Url Mappings for the Author View of the CPMS website. 

urlpatterns = [
    path('logout', views.logout, name='logout'),
    path('authorModifyInfo', views.authorModifyInfo, name='authorModifyInfo'),
    path('authorRegisterToSubmitPaper', views.authorRegisterToSubmitPaper, name='authorRegisterToSubmitPaper'),
    path('authorSubmitPaper', views.authorSubmitPaper, name='authorSubmitPaper'),
]