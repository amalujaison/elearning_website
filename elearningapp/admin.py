from django.contrib import admin
from django.contrib import admin
from django.http import HttpResponse
from elearnapp.models import Course, Mentor, Quiz, payment
from elearnapp.models import Account

admin.site.register(Account)