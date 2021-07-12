from django.urls import path
from . import views

# Url Mappings for the Login Model of the CPMS website. 

urlpatterns = [
    path('', views.login, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('forgotPassword', views.forgotPassword, name='forgotPassword'),
]

