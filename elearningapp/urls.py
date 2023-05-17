from . import views
from django.urls import path

urlpatterns = [
    path('demo/', views.demo, name='demo'),
    path('user_reg/', views.user_reg, name='user_reg'),
    path('LOGIN/', views.LOGIN, name='LOGIN'),
    path('REGISTRATION/', views.REGISTRATION, name='REGISTRATION'),

    ]