from . import views
from django.urls import path

urlpatterns = [

    path('', views.demo, name='demo'),
    path('LOGIN/', views.LOGIN, name='LOGIN'),
    path('REGISTRATION/', views.REGISTRATION, name='REGISTRATION'),
    path('register/', views.register, name='register'),
    path('home1', views.home1, name='home1'),
    path('home2/', views.home2, name='home2'),
    path('login', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('Home/', views.Home, name='Home'),
    path('about1', views.about1, name='about1'),
    path('about2/', views.about2, name='about2'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('activity/', views.activity, name='activity'),
    path('Messages/', views.Messages, name='Messages'),
    path('course/', views.course, name='course'),
    path('coursesdetails/', views.coursesdetails, name='coursesdetails'),
    path('coursesdetailsp2/', views.coursesdetailsp2, name='coursesdetailsp2'),
    path('javaintrod/', views.javaintrod, name='javaintrod'),
    path('javaadv/', views.javaadv, name='javaadv'),
    path('freecourse/', views.freecourse, name='freecourse'),
    path('paidcourse/', views.paidcourse, name='paidcourse'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    # path('changepassword/', views.changepassword, name='changepassword'),
    # path('changepswd/', views.changepswd, name='changepswd'),



    ]
