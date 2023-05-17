from datetime import timezone

from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.


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

    def create_superuser(self, password, email):
        user = self.create_user(
            email=self.normalize_email(email),
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
    # id = models.AutoField(primary_key=True)
    # first_name = models.CharField(max_length=50, default='')
    # last_name = models.CharField(max_length=50, default='')
    # email = models.EmailField(max_length=100, unique=True)
    # contact = models.BigIntegerField(default=0)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    email = models.EmailField(max_length=20, unique=True,primary_key=True)
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
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


# class Category(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


class Mentor(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=0)
    mentor_name = models.CharField(max_length=200,primary_key=True)

    def __str__(self):
        return self.mentor_name

class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200,unique=True)
    image=models.ImageField(upload_to='images')
    video = models.FileField(upload_to='videos')
    price = models.CharField(max_length=10, default=0)
    duration = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    level = models.CharField(max_length=20)
    language = models.CharField(max_length=30)
    students = models.IntegerField()
    outcomes = models.CharField(max_length=300)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    slug = models.SlugField(default='', blank=True, max_length=500, null=True)
    publish = models.DateTimeField(default=timezone.now)


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


class Order(models.Model):
    method = (
        ('EMI', "EMI"),
        ('ONLINE', "Online"),
    )
    orderitems = models.ManyToManyField(CartItem)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, null = False, default='0')
    total = models.DecimalField(max_digits=10, default=0, decimal_places=2, verbose_name='INR ORDER TOTAL')
    emailAddress = models.EmailField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=100, null=True)
    order_id = models.CharField(max_length=100, null=True)

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        # if self.coupon:
        #     total -= self.coupon.amount
        return total


class Reviews(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    review = models.CharField(max_length=500, blank=True)
    stars=models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.user


class MyAccount1(BaseUserManager):
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


class Reg_Mentor(AbstractBaseUser):
    first_name = models.CharField(blank=True,null=True,max_length=50)
    last_name = models.CharField(blank=True,null=True,max_length=50)
    email = models.EmailField(max_length=50, unique=True,primary_key=True)
    password = models.TextField(max_length=30)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    publish = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'address', 'state', 'country']

    objects = MyAccount1()
    def __str__(self):
        return self.email


class Quiz(models.Model):
    quiz_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True,blank=True)
    QuestionNo = models.CharField(max_length=100)
    Question = models.CharField(max_length=100)
    Option1 = models.CharField(max_length=100)
    Option2 = models.CharField(max_length=100)
    Option3 = models.CharField(max_length=100)
    Option4 = models.CharField(max_length=100)
    Corrans = models.CharField(max_length=100)


    def __str__(self):
        return self.QuestionNo

    def get_url(self):
        return reverse("quize", args={self.id})


class payment(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE, null=True,blank=True)
    Cardholdername= models.CharField(blank=True,null=True,max_length=50)
    AccountNo= models.CharField(max_length=100)
    Expiry_date = models.CharField(max_length=100)
    cvv = models.CharField(max_length=100)
    course=models.ForeignKey(Course, on_delete=models.CASCADE, null=True,blank=True)
    Amount=models.CharField(max_length=100,null=True)
    publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Cardholdername


