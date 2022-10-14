# import clean as clean
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
# Create your models here.


class user_reg(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=20, unique=True,primary_key=True)
    password = models.TextField(max_length=30)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


class user_log(models.Model):
    email = models.EmailField(max_length=20, primary_key=True, unique=True)
    password = models.TextField(max_length=30)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


# class mentor_reg(models.Model):
#     name = models.CharField(max_length=30)
#     email = models.EmailField(max_length=20, unique=True)
#     password = models.TextField(max_length=30)
#     phone = models.CharField(max_length=10)
#     address = models.CharField(max_length=100)
#     state = models.CharField(max_length=20)
#     country = models.CharField(max_length=20)
#     qualification = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.email


class pyadva(models.Model):
    name = models.CharField(max_length=60)
    video = models.FileField(upload_to='videos')
    duration = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    level = models.CharField(max_length=20)
    language = models.CharField(max_length=30)
    students = models.CharField(max_length=20)
    outcomes = models.CharField(max_length=300)
    curriculum = models.CharField(max_length=300)
    mentor = models.CharField(max_length=50)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class javaintro(models.Model):
    name = models.CharField(max_length=60)
    video = models.FileField(upload_to='videos')
    duration = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    level = models.CharField(max_length=20)
    language = models.CharField(max_length=30)
    students = models.CharField(max_length=20)
    outcomes = models.CharField(max_length=300)
    curriculum = models.CharField(max_length=300)
    mentor = models.CharField(max_length=50)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class javaadva(models.Model):
    name = models.CharField(max_length=60)
    video = models.FileField(upload_to='videos',default=0)
    duration = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    level = models.CharField(max_length=20)
    language = models.CharField(max_length=30)
    students = models.CharField(max_length=30)
    outcomes = models.CharField(max_length=300)
    curriculum = models.CharField(max_length=300)
    mentor = models.CharField(max_length=50)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    # def clean(self):
    #     if self.students != '111':
    #         raise ValidationError("You can use only numbers")


class freecourses(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='images')
    category = models.CharField(max_length=30)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class pyintro(models.Model):
    name = models.ForeignKey(freecourses, on_delete=models.CASCADE, default=1)
    video = models.FileField(upload_to='videos')
    duration = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    level = models.CharField(max_length=20)
    language = models.CharField(max_length=30)
    students = models.IntegerField()
    outcomes = models.CharField(max_length=300)
    curriculum = models.CharField(max_length=300)
    mentor = models.CharField(max_length=50)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.mentor


class paidcourses(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='images')
    category = models.CharField(max_length=30)
    amount = models.CharField(max_length=200)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


# class Category(models.Model):
#     title = models.CharField(max_length=100)
#
#     def _str_(self):
#         return self.title


# class courses(models.Model):
#     name = models.CharField(max_length=40)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
#     product_image = models.ImageField(upload_to='product_image/')
#     price = models.IntegerField(default=0)
#     descrtion = models.CharField(max_length=100, default='')
#     in_stock = models.BooleanField(default=True)

    # def _str_(self):
    #     return self.name

