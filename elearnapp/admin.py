import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import user_log, freecourses, paidcourses, pyintro, pyadva, javaintro, javaadva, user_reg

# Register your models here
admin.site.register(pyintro)
admin.site.register(pyadva)
admin.site.register(javaintro)
admin.site.register(javaadva)
admin.site.register(paidcourses)


def export_details(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="freecourses.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Image', 'Category', 'Publish'])
    courses = queryset.values_list('name', 'image', 'category', 'publish')
    for i in courses:
        writer.writerow(i)
    return response


export_details.short_description = 'Export to csv'


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'category', 'publish']
    actions = [export_details]


admin.site.register(freecourses,CourseAdmin)


def export_reg(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="registration.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Password',  'Phone',  'State', 'Country'])
    registration = queryset.values_list('name', 'email', 'password',  'phone',  'state', 'country')
    for i in registration:
        writer.writerow(i)
    return response


export_reg.short_description = 'Export to csv'


class RegAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'password',  'phone',  'state', 'country']
    actions = [export_reg]


admin.site.register(user_reg,RegAdmin)


def export_log(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="login.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email', 'Password'])
    login = queryset.values_list('email', 'password')
    for i in login:
        writer.writerow(i)
    return response


export_log.short_description = 'Export to csv'


class LogAdmin(admin.ModelAdmin):
    list_display = ['email', 'password']
    actions = [export_log]


admin.site.register(user_log, LogAdmin)




