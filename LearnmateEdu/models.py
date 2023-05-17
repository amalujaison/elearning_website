# # import clean as clean
# from django.core.exceptions import ValidationError
# from django.db import models
# from django.utils import timezone
# from django import forms
# Create your models here.
from django.contrib.auth.models import _user_get_permissions, AbstractUser
from django.urls.base import reverse
from django.utils import timezone
#from importlib._common import _

from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from oscrypto._ffi import null



# Create your models here.



# class user_reg(models.Model):
#     name = models.CharField(max_length=30)
#     email = models.EmailField(max_length=20, unique=True,primary_key=True)
#     password = models.TextField(max_length=30)
#     phone = models.CharField(max_length=10)
#     address = models.CharField(max_length=100)
#     state = models.CharField(max_length=20)
#     country = models.CharField(max_length=20)
#     publish = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.email
#
#
class user_log(models.Model):
    email = models.EmailField(max_length=20, primary_key=True, unique=True)
    password = models.TextField(max_length=30)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

class mentor_log(models.Model):
    email = models.EmailField(max_length=20, primary_key=True, unique=True)
    password = models.TextField(max_length=30)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
class company_log(models.Model):
    email = models.EmailField(max_length=20, primary_key=True, unique=True)
    password = models.TextField(max_length=30)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
class MyAccount(BaseUserManager):
    def create_user(self, first_name, last_name, email,  phone, address, state, country, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            # username = username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            state=state,
            country=country,
            address=address,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            **extra_fields,
            # username = username,
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(blank=True,null=True,max_length=50)
    last_name = models.CharField(blank=True,null=True,max_length=50)
    email = models.EmailField(max_length=50, unique=True,primary_key=True)
    password = models.TextField(max_length=30)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    # publish = models.DateTimeField(default=timezone.now)
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'address', 'state', 'country']
    # REQUIRED_FIELDS = ['password']

    objects = MyAccount()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return self.is_admin

    def get_all_permissions(user=None):
        if user.is_superadmin:
            return set()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Mentor(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=0)
    mentor_name = models.CharField(max_length=200,primary_key=True)

    def __str__(self):
        return self.mentor_name


class Author(models.Model):
    author_profile = models.ImageField(upload_to='images')
    name = models.CharField(max_length=200, null=True)
    profession= models.CharField(max_length=200, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name

class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200,unique=True)
    image=models.ImageField(upload_to='images')
    price = models.IntegerField()
    description = models.TextField(max_length=500)
    level = models.CharField(max_length=20)
    language = models.CharField(max_length=30)
    students = models.IntegerField()
    mentor = models.ForeignKey(Author,on_delete=models.CASCADE)
    slug = models.SlugField(default='', blank=True, max_length=500, null=True)
    publish = models.DateTimeField(default=timezone.now)
    completed_by = models.ManyToManyField(Account, blank=True)

    def __str__(self):
        return self.course_name

    def get_url(self):
        return reverse("course_details",args={self.slug})


def create_slug(instance, new_slug=None):
    slug = slugify(instance.course_name)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver,Course)


# class Cart(models.Model):
#     user = models.ForeignKey(Account, on_delete=models.CASCADE)
#     product = models.ForeignKey(Course, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
#
#
#     def get_product_price(self):
#         price = [self.product.price]
#         return sum(price)
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="media",null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=200)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class what_you_learn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points


class requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points


class CartItem(models.Model):
    cart_id = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Course, on_delete=models.CASCADE, null=True,blank=True)
    purchase = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images',null=True)

    def __str__(self):
        return f'{self.item}'

    def get_product_price(self):
        price=[self.item.price]
        return sum(price)


# class Order(models.Model):
#     method = (
#         ('EMI', "EMI"),
#         ('ONLINE', "Online"),
#     )
#     orderitems = models.ManyToManyField(CartItem)
#     user = models.ForeignKey(Account, on_delete=models.CASCADE)
#     ordered = models.BooleanField(default=False)
#     phone = models.CharField(max_length=10, null = False, default='0')
#     total = models.DecimalField(max_digits=10, default=0, decimal_places=2, verbose_name='INR ORDER TOTAL')
#     emailAddress = models.EmailField(max_length=250, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     payment_id = models.CharField(max_length=100, null=True)
#     order_id = models.CharField(max_length=100, null=True)
#
#     def get_totals(self):
#         total = 0
#         for order_item in self.orderitems.all():
#             total += float(order_item.get_total())
#         # if self.coupon:
#         #     total -= self.coupon.amount
#         return total
#

class Reviews(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    review = models.CharField(max_length=500, blank=True)
    stars=models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.user








# class LearnmateEdu(models.Model):
#     user=models.ForeignKey(Account, on_delete=models.CASCADE, null=True,blank=True)
#     Cardholdername= models.CharField(blank=True,null=True,max_length=50)
#     AccountNo= models.CharField(max_length=100)
#     Expiry_date = models.CharField(max_length=100)
#     cvv = models.CharField(max_length=100)
#     course=models.ForeignKey(Course, on_delete=models.CASCADE, null=True,blank=True)
#     Amount=models.CharField(max_length=100,null=True)
#     publish = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.Cardholdername


# class Student_Feedback(models.Model):
#     user_id=models.ForeignKey(Account, on_delete=models.CASCADE, null=True,blank=True)
#     feedback= models.TextField()
#     feedback_reply = models.TextField()
#     created_at= models.DateTimeField(auto_now_add=True,null=True)
#     updated_at = models.DateTimeField(auto_now_add=True, null=True)




class Job(models.Model):
    job_name = models.CharField(max_length=200,unique=True)
    job_image=models.ImageField(upload_to='media/images')
    job_salary = models.IntegerField(default=0)
    job_type = models.CharField(max_length=20)
    job_location = models.CharField(max_length=10)
    slug = models.SlugField(default='', blank=True, max_length=500, null=True)
    job_date = models.DateField(auto_now=True)
    job_description = models.CharField(max_length=300,default=null)
    job_responsibility = models.CharField(max_length=300,default=null)
    job_qualifications = models.CharField(max_length=300,default=null)
    applicant_name = models.CharField(max_length=50,default=null)
    applicant_email = models.EmailField(max_length=30,default=null)
    resume = models.FileField(upload_to='media/resumes/',default=null)
    def __str__(self):
        return self.job_name

    def get_url(self):
        return reverse("course_details",args={self.slug})


class Reg_Mentor(AbstractBaseUser):
    first_name = models.CharField(blank=True,null=True,max_length=50)
    last_name = models.CharField(blank=True,null=True,max_length=50)
    email = models.EmailField(max_length=50, unique=True,primary_key=True)
    password = models.TextField(max_length=30)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    # publish = models.DateTimeField(default=timezone.now)
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'address', 'state', 'country']
    # REQUIRED_FIELDS = ['password']

    objects = MyAccount()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return self.is_admin

    def get_all_permissions(user=None):
        if user.is_superadmin:
            return set()


class MyAccount1(BaseUserManager):
    def create_user(self,company_name, company_email, company_phone,company_address, company_country, company_password=None):
        if not company_email:
            raise ValueError('User must have an email address')

        user = self.model(
            company_email=self.normalize_email(company_email),
            company_name=company_name,
            company_phone=company_phone,
            company_country=company_country,
            company_address=company_address,

        )

        user.set_password(company_password)
        user.save(using=self._db)
        return user


class Reg_company(AbstractUser):
    company_name = models.CharField(blank=True,null=True,max_length=50)
    company_email = models.EmailField(max_length=50, unique=True,primary_key=True)
    password = models.CharField(max_length=100,default=True)
    company_phone = models.TextField(max_length=30)
    company_address = models.CharField(max_length=100)
    company_country = models.CharField(max_length=20)
    publish = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'company_email'
    REQUIRED_FIELDS = ['company_name', 'company_phone ', 'company_address', 'company_email', 'company_country']

    objects = MyAccount1()
    def __str__(self):
        return self.company_email


class UserCourse(models.Model):
    user = models.ForeignKey(Account, null = False , on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null = False , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course or ''


class Payment(models.Model):
    order_id = models.CharField(max_length= 50 , null = False,default='')
    payment_id = models.CharField(max_length= 50,default='')
    user_course = models.ForeignKey(UserCourse, null = True, blank = True ,  on_delete=models.CASCADE)
    user = models.ForeignKey(Account,  on_delete=models.CASCADE,default='')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,default='')
    date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)


class Order(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,default=0)
    order_id = models.CharField(max_length=100,default=0)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.email} for {self.course.course_name} ({self.amount} INR)"


class VideoProgress(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('video_detail', args=[str(self.video.course.id), str(self.video.id)])
class UserProgress(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
class Certificate(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_On = models.DateTimeField(auto_now_add=True)
    certificate_image = models.ImageField(upload_to='certificates/')

    def __str__(self):
        return self.course

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,default='')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='media/coursematerials/')

    def __str__(self):
        return self.course

class Course_material(models.Model):
    course = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='media/coursematerials/')

class Quiz_save(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,primary_key=True,unique=True)
    question1 = models.CharField(max_length=255,null=True)
    answer1 = models.CharField(max_length=255,null=True)
    question2 = models.CharField(max_length=255, null=True)
    answer2 = models.CharField(max_length=255, null=True)
    question3 = models.CharField(max_length=255, null=True)
    answer3 = models.CharField(max_length=255, null=True)
    question4 = models.CharField(max_length=255, null=True)
    answer4 = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.course

class Apply_job(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE,default='',null=True)
    applicant_name = models.CharField(max_length=50,default=null)
    applicant_email = models.EmailField(max_length=30,default=null)
    resume = models.FileField(upload_to='resumes',default=null)
    def __str__(self):
        return self.job

class Enrollment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course

class Save_quiz(models.Model):
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE,unique=True,default='')
    question1 = models.CharField(max_length=255,null=True)
    answer1 = models.CharField(max_length=255,null=True)
    question2 = models.CharField(max_length=255, null=True)
    answer2 = models.CharField(max_length=255, null=True)
    question3 = models.CharField(max_length=255, null=True)
    answer3 = models.CharField(max_length=255, null=True)
    question4 = models.CharField(max_length=255, null=True)
    answer4 = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.course

class table_quiz(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE,default='')
    question1 = models.CharField(max_length=255, null=True)
    answer1 = models.CharField(max_length=255, null=True)
    question2 = models.CharField(max_length=255, null=True)
    answer2 = models.CharField(max_length=255, null=True)
    question3 = models.CharField(max_length=255, null=True)
    answer3 = models.CharField(max_length=255, null=True)
    question4 = models.CharField(max_length=255, null=True)
    answer4 = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.course

# class Quiz(models.Model):
#
#     Question = models.CharField(max_length=100)
#     Option1 = models.CharField(max_length=100)
#     Option2 = models.CharField(max_length=100)
#     Option3 = models.CharField(max_length=100)
#     Option4 = models.CharField(max_length=100)
#     Corrans = models.CharField(max_length=100)
#
#
#     def __str__(self):
#         return self.QuestionNo

class QuizResult(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    quiz = models.ForeignKey(table_quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    percent = models.DecimalField(max_digits=5, decimal_places=2,default=1)

