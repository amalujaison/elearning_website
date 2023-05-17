import io
from _sha256 import sha256
from datetime import time
from io import BytesIO
import razorpay
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.context_processors import request
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Course, UserProgress, Certificate, CourseMaterial, Course_material, mentor_log, Apply_job, \
    Enrollment, Save_quiz, table_quiz, QuizResult

from .models import Account, Category, Course, CartItem, Reviews, Mentor, \
    what_you_learn, requirements, Job, UserCourse, Payment, user_log, Reg_company, company_log, Video
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from PIL import Image, ImageDraw, ImageFont
import os
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from cart.cart import Cart
import razorpay

# from elearning.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY

from .models import Reg_Mentor
from .models import Quiz_save



# from .LearnmateEdu.views import client


# from hashlib import sha256
#
# from django.contrib import messages
# from django.shortcuts import render, redirect
#
#
# from elearnapp.models import user_reg, user_log, freecourses, paidcourses, pyintro, pyadva, javaintro, javaadva
#
#
# # Create your views here.
#
#
def demo(request):
    course = Course.objects.all()
    categories = Category.objects.all()
    review = Reviews.objects.all()
    return render(request, "index.html", {'course': course, 'categories': categories, 'review': review})


def home1(request):
    return render(request, "index.html")


def Home_mentor(request):
    course = Course.objects.all()
    categories = Category.objects.all()
    review = Reviews.objects.all()
    return render(request, "Home-mentor.html", {'course': course, 'categories': categories, 'review': review})


def LOGIN(request):
    return render(request, "LOGIN.html")


def base(request):
    return render(request, "base.html")


#
#
def REGISTRATION(request):
    return render(request, "REGISTRATION.html")


#
#


def Home(request):
    course = Course.objects.all()
    categories = Category.objects.all()
    review = Reviews.objects.all()
    return render(request, "Home.html", {'course': course, 'categories': categories, 'review': review})


#

#
def home(request):
    if 'email' in request.session:
        email = request.session['email']
        return render(request, 'Home.html', {'email': email})
    return redirect(login)


#
#
def about1(request):
    return render(request, "about-1.html")


def about2(request):
    return render(request, "about-2.html")


def userprofile(request):
    return render(request, "user-profile.html")


def reports(request):
    return render(request, "Reports.html")


def activity(request):
    return render(request, "list-view-calendar.html")


def Messages(request):
    return render(request, "mailbox.html")


def course(request):
    return render(request, "paid courses.html")


def category(request):
    obj = category.objects.all()
    return render(request, "courses-details.html", {'result': obj})


def course_detail(request):
    obj = Course.objects.all()
    return render(request, "courses-details.html", {'result': obj})


# def error(request):
#     # category = Category.objects.filter(Category)
#     return render(request, "error-404.html", {'category': category})


# def javaadv(request):
#     obj=course.objects.all()
#     return render(request,"java1.html",{'result':obj})


# Create your views here.


# def demo(request):
#     return render(request,"index.html")
#
#
# def LOGIN(request):
#     return render(request,"LOGIN.html")
#
# def REGISTRATION(request):
#     return render(request, "REGISTRATION.html")
#
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = auth.authenticate(email=email, password=password)
        print(user)

        if user is not None:
            auth.login(request, user)
            # save email in session
            request.session['email'] = email

            if user.is_active:
                return redirect('Home')

            else:
                return redirect('REGISTRATION')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('LOGIN')
    return render(request, 'LOGIN.html')


def user_reg(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        # username = email.split('@')[0]
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        address = request.POST.get('address')
        state = request.POST.get('state')
        country = request.POST.get('country')
        if Account.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('user_reg')
        user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone=phone,
                                           address=address, state=state, country=country,
                                           password=password)
        user.is_user = True
        user.save()
        messages.info(request, 'Thank you for registering with us. Please Login')
        return redirect('LOGIN')
    return render(request, 'REGISTRATION.html')


def logout(request):
    auth.logout(request)
    return redirect('demo')


@login_required
def changepassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact=request.user.email)
        success = user.check_password(current_password)
        if success:
            user.set_password(new_password)
            user.save()
            messages.info(request, 'Password updated successfully.')
            return redirect('LOGIN')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('changepassword')
    return render(request, 'Change_Password.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email

            current_site = get_current_site(request)
            message = render_to_string('ResetPassword_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(
                'Please activate your account',
                message,
                'learnmateedu@gmail.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('LOGIN')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'Forgot_Password.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('LOGIN')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('LOGIN')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'ResetPassword.html')


def courses(request):
    obj = Course.objects.all()
    return render(request, "paid courses.html", {'result': obj})


def courses_mentor(request):
    obj = Course.objects.all()
    return render(request, "paid courses-mentor.html", {'result': obj})


def course_details(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    point = what_you_learn.objects.all()
    req = requirements.objects.all()
    context = {
        'course': course,
        'results': point,
        'res': req,

    }
    return render(request, "course-details-before enrolling.html", context)


# def course_details(request, slug):
#     course = Course.objects.get(slug=slug)
#     videos = Video.objects.filter(course=course).order_by('order')
#     user_progress = {up.video_id: up for up in UserProgress.objects.filter(user=request.user)}
#     context = {
#         'course': course,
#         'videos': videos,
#         'user_progress': user_progress,
#     }
#     return render(request, 'course_details.html', context)
from django.db.models import Count
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# def recommend_courses(user):
#     # Get the courses that the user has already taken
#     courses_taken = user.course_set.all().values_list('id', flat=True)
#
#     # Get all other courses
#     other_courses = Course.objects.exclude(id__in=courses_taken)
#
#     # Create a matrix of interactions between the user and the courses
#     interactions = np.zeros((other_courses.count(),))
#     for i, course in enumerate(other_courses):
#         interactions[i] = 1 if user in course.students.all() else 0
#
#     # Compute the similarity between the user's interactions and those of other users
#     matrix = np.zeros((other_courses.count(), other_courses.count()))
#     for i, course1 in enumerate(other_courses):
#         for j, course2 in enumerate(other_courses):
#             if i == j:
#                 matrix[i, j] = 1.0
#             else:
#                 x = interactions[i]
#                 y = interactions[j]
#                 matrix[i, j] = x * y
#
#     # Find the courses that are most similar to the user's interactions
#     sims = matrix.sum(axis=1)
#     idx = np.argsort(sims)[::-1]
#     top_courses = [other_courses[j] for j in idx][:5]  # take top 5
#
#     # Return the recommended courses
#     return top_courses
# def course_details(request, course_slug):
#     course = get_object_or_404(Course, slug=course_slug)
#     recommended_courses = recommend_courses(course)
#     points = what_you_learn.objects.filter(course=course)
#     reqs = requirements.objects.filter(course=course)
#     context = {
#         'course': course,
#         'points': points,
#         'reqs': reqs,
#         'recommended_courses':recommended_courses,
#     }
#     return render(request, "course-single-v4.html", context)
#
# # Cart functions
# def recommend_courses(account):
#     # Get the courses that the user has already taken
#     courses_taken = account.user_courses.all().values_list('id', flat=True)
#
#     # Get all other courses
#     other_courses = Course.objects.exclude(id__in=courses_taken)
#
#     # Create a matrix of interactions between the user and the courses
#     interactions = np.zeros((other_courses.count(),))
#     for i, course in enumerate(other_courses):
#         interactions[i] = 1 if account in course.students.all() else 0
#
#     # Compute the similarity between the user's interactions and those of other users
#     matrix = np.zeros((other_courses.count(), other_courses.count()))
#     for i, course1 in enumerate(other_courses):
#         for j, course2 in enumerate(other_courses):
#             if i == j:
#                 matrix[i, j] = 1.0
#             else:
#                 x = interactions[i]
#                 y = interactions[j]
#                 matrix[i, j] = x * y
#
#     # Find the courses that are most similar to the user's interactions
#     sims = matrix.sum(axis=1)
#     idx = np.argsort(sims)[::-1]
#     top_courses = [other_courses[j] for j in idx][:5]  # take top 5
#
#     # Return the recommended courses
#     return top_courses
@login_required
# def course_details(request, course_slug):
#     course = get_object_or_404(Course, slug=course_slug)
#     recommended_courses = recommend_courses(request.user)
#     points = what_you_learn.objects.filter(course=course)
#     reqs = requirements.objects.filter(course=course)
#     context = {
#         'course': course,
#         'points': points,
#         'reqs': reqs,
#         'recommended_courses':recommended_courses,
#     }
#     return render(request, "course-single-v4.html", context)
# def course_details(request, course_slug):
#     course = get_object_or_404(Course, slug=course_slug)
#     recommended_courses = recommend_courses(request.user.first_name)
#     points = what_you_learn.objects.filter(course=course)
#     reqs = requirements.objects.filter(course=course)
#     context = {
#         'course': course,
#         'points': points,
#         'reqs': reqs,
#         'recommended_courses':recommended_courses,
#     }
#     return render(request, "course-single-v4.html", context)

# def course_details(request, course_slug):
#     course = get_object_or_404(Course, slug=course_slug)
#     recommended_courses = []
#     if request.user is not None and hasattr(request.user, 'user_courses'):
#         recommended_courses = recommend_courses(request.user.first_name)
#     points = what_you_learn.objects.filter(course=course)
#     reqs = requirements.objects.filter(course=course)
#     context = {
#         'course': course,
#         'points': points,
#         'reqs': reqs,
#         'recommended_courses': recommended_courses,
#     }
#     return render(request, "course-single-v4.html", context)

# def recommend_courses(course_name):
#     # Find the course with the given name
#     course = get_object_or_404(Course, name=course_name)
#
#     # Find courses that are similar to the input course
#     similar_courses = Course.objects.filter(Q(category=course.category) | Q(tags__in=course.tags.all())).exclude(id=course.id)
#
#     # Sort the courses by relevance and return the recommended courses
#     recommended_courses = similar_courses.annotate(relevance=Count('category') + Count('tags')).order_by('-relevance')[:5]
#
#     return recommended_courses

# def recommend_courses(course_name):
#     # Find the course with the given name
#     course = Course.objects.values_list('course_name', flat=True).first()
#
#     # Find courses that are similar to the input course
#     similar_courses = Course.objects.filter(category=course.category).exclude(id=course.id)
#
#     # Sort the courses by relevance and return the recommended courses
#     recommended_courses = similar_courses.annotate(relevance=Count('category')).order_by('-relevance')[:5]
#
#     return recommended_courses
#
# def course_details(request, course_slug):
#     course = Course.objects.values_list('course_name', flat=True).first()
#     recommended_courses = []
#
#     # Check if request.user is a valid user object
#     if request.user.is_authenticated and hasattr(request.user, 'user_courses'):
#         recommended_courses = recommend_courses(course.name)
#     context = {
#         'course': course,
#
#         'recommended_courses': recommended_courses,
#     }
#     return render(request, "course-single-v4.html", context)
@login_required
def add_cart(request, id):
    if 'email' in request.session:
        item = Course.objects.get(id=id)
        user = request.session['email']
        if CartItem.objects.filter(user_id=user, cart_id=item).exists():

            return redirect('view_cart')
        else:
            price = item.price
            new_cart = CartItem(user_id=user, cart_id=item, price=price)
            new_cart.save()

            return redirect('view_cart')
    messages.success(request, "Product is added in your cart.")
    return render(request, 'Cart/Cart1.html')


#
# Cart Quentity Plus Settings
# Cart View page
@login_required
def view_cart(request):
    if 'email' in request.session:
        email = request.session['email']
        # price = item.price
        # item = Course.objects.filter()
        #
        # price= item.price
        user = request.user
        cart = CartItem.objects.filter(user_id=email)
        amount = 0.0
        cart_product = [p for p in CartItem.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                subtotal = p.price + amount
            messages.warning(request, "This product is added to your cart")
            return render(request, 'Cart/Cart1.html', {'cart': cart, 'subtotal': subtotal})
        else:
            return render(request, 'Cart/Cart1.html')


# Remove Items From Cart
def de_cart(request, id):
    email = request.session['email']
    cart = CartItem.objects.filter(user_id=email)
    if cart.exists():
        CartItem.objects.get(id=id).delete()
        messages.warning(request, "This product is removed form your cart")
        # messages.info(request, "You don't have an active order")
        return redirect('view_cart')
    # if ObjectDoesNotExist():
    #     messages.info(request, "You don't have an active order")
    #     return redirect("Home")


def profile(request):
    return render(request, "user-profile.html")


# def review(request):
#     return render(request,"mailbox-compose.html")


def update_profile(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        state = request.POST.get('state')
        country = request.POST.get('country')
        user_email = request.user.email

        user = Account.objects.get(email=user_email)
        user.first_name = first_name
        user.last_name = last_name
        # user.email = email
        user.phone = phone
        user.address = address
        user.state = state
        user.country = country
        print(user_email)
        # if password != None and password != "":
        #     user.set_password(password)
        user.save()
        messages.success(request, 'Profile Is Successfully Updated. ')
        return redirect('profile')


def search_course(request):
    query = request.GET['query']
    course = Course.objects.filter(course_name__icontains=query)
    context = {
        'course': course,
    }
    return render(request, 'search.html', context)


# def usercertificate(request):
#     if request.method == "POST":
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         user = Account.objects.filter()
#         course = Course.objects.filter().first()
#         context = {
#             'course': course,
#             'user': user,
#             'first_name': first_name,
#             'last_name': last_name,
#         }
#         return render(request,"certificate.html",context)
#
#
# # def render_to_pdf(template_src, context_dict={}):
# #     template = get_template(template_src)
# #     html  = template.render(context_dict)
# #     result = BytesIO()
# #     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
# #     if not pdf.err:
# #         return HttpResponse(result.getvalue(), content_type='application/pdf')
# #     return None
#
#
# # def usercertificate(request, course_slug):
# #     posts = Course.objects.filter(slug=course_slug).first()
# #     # category = Category.objects.filter(slug=slug)
# #     carts = CartItem.objects.filter(user=request.user, purchase=False)
# #
# #     if carts.exists():
# #         return render_to_pdf('certificate.html',{'customerName':request.user.first_name,'customerNamelast':request.user.last_name,
# #         'customerEmail':request.user.email,'carts':carts,'posts':posts})
# #
# #     return render_to_pdf('certificate.html', {'posts':posts})


# def render_to_pdf(template_src, context_dict):
#     template = get_template(template_src)
#     html = template.render(context_dict)
#     result = io.BytesIO()
#     pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return


def usercertificate(request):
    posts = Course.objects.filter().first()

    carts = CartItem.objects.filter(user=request.user, purchase=False)

    if carts.exists():
        return render_to_pdf('certificate.html',
                             {'customerName': request.user.first_name, 'customerNamelast': request.user.last_name,
                              'customerEmail': request.user.email, 'carts': carts, 'posts': posts})

    return render_to_pdf('certificate.html', {'posts': posts})


def certificate(request):
    course = Course.objects.all()
    return render(request, 'certificate.html',
                  {'customerName': request.user.first_name, 'customerNamelast': request.user.last_name,
                   'customerEmail': request.user.email})


def test(request):
    return render(request, "TEST.html")


# def payments(request):
#     if request.method == "POST":
#      order_amount = 100
#      order_currency = "INR"
#      payment_order = client.order.create(dict(amount=order_amount,currency=order_currency,payment_capture =1))
#      payment_order_id = payment_order['id']
#      Cardholdername = request.POST.get('name')
#      AccountNo = request.POST.get('number')
#      Expiry_date = request.POST.get('exp')
#      cvv = request.POST.get('cvv')
#      Amount = request.POST.get('amount')
#      user_email = request.user.email
#      users = Account.objects.get(email=user_email)
#      context = {
#                  'Cardholdername':Cardholdername,
#                  'AccountNo':AccountNo,
#                  'Expiry_date':Expiry_date,
#                  'cvv':cvv,
#                  'Amount':Amount,
#                  'user':users,
#                  'api_key' :RAZORPAY_API_KEY,
#                  'order_id' :payment_order_id,
#                      }
#     return render(request,context,"LearnmateEdu.html")


def payments(request):
    context = {}
    if request.method == "POST":
        order_amount = 100
        order_currency = "INR"
        payment_order = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture=1))
        payment_order_id = payment_order['id']
        Cardholdername = request.POST.get('name')
        AccountNo = request.POST.get('number')
        Expiry_date = request.POST.get('exp')
        cvv = request.POST.get('cvv')
        Amount = request.POST.get('amount')
        user_email = request.user.email
        users = Account.objects.get(email=user_email)
        context.update({
            'Cardholdername': Cardholdername,
            'AccountNo': AccountNo,
            'Expiry_date': Expiry_date,
            'cvv': cvv,
            'Amount': Amount,
            'user': users,
            'api_key': RAZORPAY_API_KEY,
            'order_id': payment_order_id,
        })
    return render(request, "LearnmateEdu.html", context)


def Review(request):
    if request.method == "POST":
        stars = request.POST.get('stars')
        review = request.POST.get('review')
        user_email = request.user.email

        users = Account.objects.get(email=user_email)
        user = Reviews(stars=stars, review=review, user=users)
        user.save()
        messages.info(request, 'Your review has been successfully send..!!')
        return redirect('Review')
    return render(request, 'mailbox-compose.html')


# def mentor_reg(request):
#     if request.method == "POST":
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         phone = request.POST.get('phone')
#         address = request.POST.get('address')
#         state = request.POST.get('state')
#         country = request.POST.get('country')
#         paswd = sha256(password.encode()).hexdigest()
#         mentor = mentor_reg(first_name=first_name,last_name=last_name,email=email,password=paswd,phone=phone,address=address,state=state,country=country)
#         # log = user_log(email=email,password=paswd)
#         mentor.save()
#         # log.save()
#         messages.info(request, 'Your account has been successfully created..!!')
#         return redirect('mentor_login')
#     return render(request, 'REGISTRATION-Mentor.html')


# def mentor_login(request):
#     if request.method == 'POST':
#         email = request.POST('email')
#         password = request.POST('password')
#         print(email, password)
#         user = auth.authenticate(email=email, password=password)
#         print(user)
#
#         if user is not None:
#             auth.login(request, user)
#             # save email in session
#             request.session['email'] = email
#
#             if user.is_active:
#                 return redirect('Home')
#
#             else:
#                 return redirect('mentor_reg')
#         else:
#             messages.error(request, 'Invalid Credentials')
#             return redirect('mentor_login')
#     return render(request, 'LOGIN-company.html')


def update_profilementor(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        state = request.POST.get('state')
        country = request.POST.get('country')
        user_email = request.user.email

        user = Reg_Mentor.objects.get(email=user_email)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone
        user.address = address
        user.state = state
        user.country = country
        print(user_email)
        # if password != None and password != "":
        #     user.set_password(password)
        user.save()
        messages.success(request, 'Profile Is Successfully Updated. ')
        return redirect('profile')


# def quiz(request, id):
#     if request.method == 'POST':
#         # print(request.POST)
#         course = Course.objects.get(id)
#         questions = Quiz.objects.filter()
#         score = 0
#
#         wrong = 0
#         correct = 0
#         total = 0
#         for q in questions:
#             total += 1
#             # print(total)
#             print(q.question1)
#             print(q.answer1)
#             print(request.POST.get(q.answer1))
#
#             print()
#             if q.Corrans == request.POST.get(q.answer1):
#                 score += 10
#                 correct += 1
#             else:
#                 wrong += 1
#                 print(wrong)
#         percent = score / (total * 10) * 100
#         context = {
#             'score': score,
#             'time': request.POST.get('timer'),
#             'correct': correct,
#             'wrong': wrong,
#             'percent': percent,
#             'total': total,
#             'course': course,
#         }
#         return render(request, 'result.html', context)
#     else:
#         questions = Quiz.objects.all()
#         context = {
#             'questions': questions
#         }
#         return render(request, 'Quiz.html', context)
# #
#
# def quize(request, id):
#     single = Quiz.objects.get(id=id)
#
#     context = {
#         'result': single,
#
#     }
#     return render(request, "Quiz.html", context)


# def company_registration(request):
#     if request.method == 'POST':
#         company_name = request.POST.get('last_name')
#         company_email = request.POST.get('email')
#         company_phone = request.POST.get('phone')
#         company_password = request.POST.get('password')
#         company_address = request.POST.get('address')
#         company_country = request.POST.get('country')
#         # if mentor_reg.objects.filter(email=email).exists():
#         #     messages.error(request, 'Email already exists')
#         #     return redirect('user_reg')
#         user = Reg_company.objects.create_user(company_name=company_name, company_email=company_email,company_password=company_password, company_phone=company_phone,company_address=company_address, company_country=company_country)
#         user.is_user = True
#         user.save()
#         messages.info(request, 'Thank you for registering with us. Please Login')
#         return redirect('company_login')
#     return render(request, 'REGISTRATION-company.html')
#
#
# def company_login(request):
#     if request.method == 'POST':
#         company_email = request.POST.get('email')
#         company_password = request.POST.get('password')
#         print(company_email, company_password)
#
#         user = auth.authenticate(company_email=company_email, company_password=company_password)
#         print(user)
#         if user is not None:
#             auth.login(request, user)
#             # save email in session
#             request.session['email'] = company_email
#
#             if user.is_active:
#                 return redirect('forms')
#             else:
#                 return redirect('company_registration')
#         else:
#             messages.error(request, 'Invalid email or password.')
#             return redirect('company_login')
#     return render(request, 'LOGIN-company.html')
#


# def mentor_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(email, password)
#         user = auth.authenticate(email=email, password=password)
#         print(user)
#
#         if user is not None:
#             auth.login(request, user)
#             # save email in session
#             request.session['email'] = email
#
#             if user.is_user:
#                 return redirect('Home')
#
#             else:
#                 return redirect('company_registration')
#         else:
#             messages.error(request, 'Invalid Credentials')
#             return redirect('company_login')
#     return render(request, 'LOGIN-company.html')
#
def Learner_dashboard(request):
    return render(request, 'dashboard_user.html')


def doubts(request):
    return render(request, 'doubts.html')


# @csrf_exempt
# def razorpay_payment(request):
#     if request.method == 'POST':
#         amount = request.POST.get('amount')
#         client = razorpay.Client(auth=('your_key', 'your_secret'))
#         LearnmateEdu = client.order.create({'amount': amount, 'currency': 'INR'})
#         return JsonResponse(LearnmateEdu)
#
#
# @csrf_exempt
# def razorpay_confirm(request):
#     if request.method == 'POST':
#         payment_id = request.POST.get('razorpay_payment_id')
#         client = razorpay.Client(auth=('your_key', 'your_secret'))
#         LearnmateEdu = client.order.fetch(payment_id)
#         if LearnmateEdu['status'] == 'authorized':
#             # Enroll the user in the course
#             # ...
#             return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'failure'})


def job_list(request):
    obj1 = Job.objects.all()
    return render(request, "job-list.html", {'result1': obj1})


def job_index(request):
    return render(request, 'index-job.html')


def job_detail(request):
    obj = Job.objects.all()
    return render(request, 'job-detail.html',{'result': obj})


def company_adminpanel(request):
    return render(request, 'add_jobs.html')


def forms(request):
    return render(request, 'forms.html')


def Job_add(request):
    if request.method == "POST":
        job_name = request.POST.get('jobname')
        job_image = request.FILES.get('image')
        job_location = request.POST.get('joblocation')
        job_type = request.POST.get('jobtype')
        job_salary = request.POST.get('jobsalary')
        job_date = request.POST.get('date')
        job_description = request.POST.get('jobdescription')
        job_responsibility = request.POST.get('jobrequirements')
        job_qualifications = request.POST.get('jobqualification')

        jobs = Job(job_name=job_name, job_image=job_image, job_location=job_location, job_type=job_type,
                   job_salary=job_salary, job_date=job_date, job_description=job_description,
                   job_responsibility=job_responsibility, job_qualifications=job_qualifications)
        jobs.save()
        messages.info(request, 'Job added successfully..!!')
        return redirect('Job_add')
    return render(request, 'forms.html')


# def mentor_registration(request):
#     if request.method == 'POST':
#         company_name = request.POST.get('last_name')
#         company_email = request.POST.get('email')
#         company_phone = request.POST.get('phone')
#         company_password = request.POST.get('password')
#         company_address = request.POST.get('address')
#         company_country = request.POST.get('country')
#         # if mentor_reg.objects.filter(email=email).exists():
#         #     messages.error(request, 'Email already exists')
#         #     return redirect('user_reg')
#         user = Reg_company.objects.create_user(company_name=company_name, company_email=company_email,
#                                                company_phone=company_phone, company_address=company_address,
#                                                company_country=company_country,
#                                                company_password=company_password)
#         user.is_user = True
#         user.save()
#         messages.info(request, 'Thank you for registering with us. Please Login')
#         return redirect('LOGIN')
#     return render(request, 'REGISTRATION-company.html')


# @login_required(login_url='/login')
# def checkout(request,course_slug):
#     course = Course.objects.get(slug=course_slug)
#     user = request.user
#     action = request.GET.get('action')
#     order = None
#     LearnmateEdu = None
#     error = None
#     try:
#         user_course = UserCourse.objects.get(user=user, course=course)
#         error = "You are Already Enrolled in this Course"
#     except:
#         pass
#     amount = None
#     if error is None:
#         amount = int((course.price - (course.price * course.discount * 0.01)) * 100)
#     # if ammount is zero don't create paymenty , only save emrollment obbect
#
#     if amount == 0:
#         userCourse = UserCourse(user=user, course=course)
#         userCourse.save()
#         return redirect('my-courses')
#         # enroll direct
#     if action == 'create_payment':
#         currency = "INR"
#         notes = {
#             "email": user.email,
#             "name": f'{user.first_name} {user.last_name}'
#         }
#         reciept = f"codewithvirendra-{int(time())}"
#         order = client.order.create(
#             {'receipt': reciept,
#              'notes': notes,
#              'amount': amount,
#              'currency': currency
#              }
#         )
#
#         LearnmateEdu = Payment()
#         LearnmateEdu.user = user
#         LearnmateEdu.course = course
#         LearnmateEdu.order_id = order.get('id')
#         LearnmateEdu.save()
#
#     context = {
#         "course": course,
#         "order": order,
#         "LearnmateEdu": LearnmateEdu,
#         "user": user,
#         "error": error
#     }
#     return render(request, template_name="checkout/check out1.html", context=context)
#


def mentor_registration(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        state = request.POST['state']
        country = request.POST['country']
        paswd = sha256(password.encode()).hexdigest()
        user = user_reg(name=name, email=email, password=paswd, phone=phone, address=address, state=state,
                        country=country)
        log = mentor_log(email=email, password=paswd)
        user.save()
        log.save()
        messages.info(request, 'Your account has been successfully created..!!')
        return redirect('mentor_login')
    return render(request, 'REGISTRATION.html')


# Login Function


def mentor_login(request):
    request.session.flush()
    if 'email' in request.session:
        return redirect(home)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = sha256(password.encode()).hexdigest()
        user = mentor_log.objects.filter(email=email, password=password2)
        if user:
            mentor_details = mentor_log.objects.get(email=email, password=password2)
            email = mentor_details.email
            request.session['email'] = email
            return redirect('mentor_dashboard')
        else:
            print("Invalid")
    return render(request, 'LOGIN.html')


def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        # username = email.split('@')[0]
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        address = request.POST.get('address')
        state = request.POST.get('state')
        country = request.POST.get('country')
        # if mentor_reg.objects.filter(email=email).exists():
        #     messages.error(request, 'Email already exists')
        #     return redirect('user_reg')
        user = Reg_Mentor.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone=phone,
                                              address=address, state=state, country=country,
                                              password=password)
        user.is_staff = True
        user.save()
        messages.info(request, 'Thank you for registering with us. Please Login')
        return redirect('LOGIN')
    return render(request, 'REGISTRATION-Mentor.html')


# def mentor_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(email, password)
#         user = auth.authenticate(email=email, password=password)
#         print(user)
#
#         if user is not None:
#             auth.login(request, user)
#             # save email in session
#             request.session['email'] = email
#
#             if user.is_user:
#                 return redirect('Home_mentor')
#
#             else:
#                 return redirect('mentor_registration')
#         else:
#             messages.error(request, 'Invalid Credentials')
#             return redirect('mentor_login')
#     return render(request, 'LOGIN-mentor.html')


def mentor_dashboard(request):
    return render(request, 'mentor_dashboard.html')


def company_registration(request):
    if request.method == 'POST':
        company_name = request.POST.get('last_name')
        company_email = request.POST.get('email')
        company_phone = request.POST.get('phone')
        company_password = request.POST.get('password')
        company_address = request.POST.get('address')
        company_country = request.POST.get('country')

        # if mentor_reg.objects.filter(email=email).exists():
        #     messages.error(request, 'Email already exists')
        #     return redirect('user_reg')
        company = Reg_company.objects.create_user(company_name=company_name, company_email=company_email,
                                                  company_password=company_password, company_phone=company_phone,
                                                  company_address=company_address, company_country=company_country)
        company.is_staff = True
        company.save()
        messages.info(request, 'Thank you for registering with us. Please Login')
        return redirect('company_login')
    return render(request, 'Registration-Company.html')


def company_login(request):
    request.session.flush()
    if 'email' in request.session:
        return redirect(home)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = sha256(password.encode()).hexdigest()
        user = company_log.objects.filter(email=email, password=password2)
        if user:
            user_details = company_log.objects.get(email=email, password=password2)
            email = user_details.email
            request.session['email'] = email
            return redirect('home')
        else:
            print("Invalid")
    return render(request, 'LOGIN.html')


def my_view(request):
    return render(request, 'Add_quiz.html')


def Add_quiz(request):
    if request.method == "POST":
        coursename = request.POST.get('coursename')
        question1= request.POST.get('question')
        answer1 = request.POST.get('answer')
        question2 = request.POST.get('question2')
        answer2 = request.POST.get('answer2')
        question3 = request.POST.get('question3')
        answer3 = request.POST.get('answer3')
        question4 = request.POST.get('question4')
        answer4 = request.POST.get('answer4')

        quize = table_quiz(course_id=coursename,question1=question1, answer1=answer1,question2=question2, answer2=answer2,question3=question3, answer3=answer3,question4=question4, answer4=answer4)
        quize.save()
        messages.info(request, 'Quiz added successfully..!!')
        return redirect('Add_quiz')
    return render(request, 'Add_quiz.html')


def watch_course(request, slug):
    course = Course.objects.filter(slug=slug)
    coursematerial=Course_material.objects.all()
    lecture = request.GET.get('lecture')
    print(lecture)
    video = None
    if lecture is not None:
        try:
            video = Video.objects.get(id=lecture)
            print(video)
        except Video.DoesNotExist:
            pass
    if course.exists():
        course = course.first()
    else:
        return redirect('error')

    context = {
        'course': course,
        'video': video,
        'coursematerial':coursematerial,
    }
    return render(request, 'watch_course.html', context)


def course_detail(request, id):
    course = Course.objects.get(id=id)
    user = request.user

    # Check if user has already completed this course
    if user in course.completed_by.all():
        completed = True
    else:
        completed = False

    context = {'course': course, 'completed': completed}
    return render(request, 'course_detail.html', context)


@login_required
def complete_course(request, id):
    course = Course.objects.get(id=id)
    user = request.user

    # Add user to completed_by field
    course.completed_by.add(user)

    return redirect('generate_certificate', id=id)


# @login_required
# def generate_certificate(request, course_id):
#     # Get the course object
#     course = Course.objects.get(id=course_id)
#
#     # Get the user object
#     user = request.user
#
#     # Check if the user has completed the course
#     if not user in course.completed_by.all():
#         return HttpResponse("You have not completed this course.")
#
#     # Generate the certificate
#     certificate_name = f"{user.first_name}_{user.last_name}_{course.title}.pdf"
#     certificate_path = os.path.join(settings.BASE_DIR, "media/certificates", certificate_name)
#
#     buffer = BytesIO()
#
#     p = canvas.Canvas(buffer)
#     p.drawString(100, 750, "Certificate of Completion")
#     p.drawString(100, 700, f"This is to certify that {user.first_name} {user.last_name} has completed the course")
#     p.drawString(100, 675, f"{course.title} with a score of {course.score} out of {course.total_score}.")
#     p.showPage()
#     p.save()
#
#     # Save the certificate as a PDF file
#     with open(certificate_path, 'wb') as f:
#         pdf = buffer.getvalue()
#         f.write(pdf)
#
#     # Render the certificate as a PDF in the browser
#     certificate = open(certificate_path, 'rb').read()
#     response = HttpResponse(content_type='application/pdf')
#     response.write(certificate)
#     response['Content-Disposition'] = f'filename="{certificate_name}"'
#     os.remove(certificate_path)
#
#     return response
@login_required
def generate_certificate(request,id):
    course = Course.objects.get(id=id)
    certificate = Certificate.objects.all()
    user_progress = Course.objects.get(course_name=course)
    if user_progress.completed_by:
        # generate certificate logic here
        return render(request, 'certificate1.html', {'course': course, 'certificate': certificate})
    else:
        return render(request, 'error.html', {'message': 'You must complete the course to generate a certificate.'})


def error(request):
    return render(request, 'error-404.html')


import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Course, Order

# Create an instance of Razorpay client with API key and secret key
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))


def payment(request, id):
    course = Course.objects.get(id=id)
    amount = int(course.price * 100)  # convert to integer
    print(type(amount))
    order = razorpay_client.order.create({'amount': amount, 'currency': 'INR'})
    order_id = order['id']
    Order.objects.create(user=request.user, course=course, order_id=order_id, amount=amount)
    return render(request, 'LearnmateEdu.html', {'order_id': order_id, 'amount': amount})


@csrf_exempt
@login_required
def payment_success(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.payment.fetch(payment_id)

        try:
            order = Order.objects.get(order_id=order_id)
            order.payment_id = payment_id
            order.signature = signature
            order.status = 'SUCCESS'
            order.user = request.user  # Set the user field to the logged-in user
            order.save()
            return render(request, 'payment_success.html')
        except Order.DoesNotExist:
            return render(request, 'payment_failure.html')
    else:
        return JsonResponse({'error': 'Invalid request'})


def payment_failure(request):
    return render(request, 'LearnmateEdu-failure.html')


def checkout(request, id):
    course = Course.objects.filter(id=id).first()
    return render(request, "checkout/check out1.html", {'result': course})


from .models import VideoProgress


@login_required
def mark_video_as_watched(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    progress, created = VideoProgress.objects.get_or_create(user=request.user, video=video)
    progress.watched = True
    progress.save()
    return JsonResponse({'success': True})


def Quiz_view(request):
    course = Course.objects.all()
    quiz = Quiz_save.objects.all()
    return render(request, "Quiz.html", {'course': course, 'quiz': quiz, })


# def quiz_check(request,id):
#     quiz = quiz_answer.objects.get(id=id)
#     if request.method == 'POST':
#         user_answers = request.POST.getlist('answer')
#         total_marks = 0
#
#         for i, answer_id in enumerate(user_answers):
#             question = get_object_or_404(quiz_answer, id=i+1)
#             selected_answer = get_object_or_404(quiz_answer, id=int(answer_id))
#
#             if selected_answer.question == question and selected_answer.selected_answer == question.correct_answer:
#                 total_marks += 1
#
#         return render(request, 'quiz_result.html', {'total_marks': total_marks})
#
#         # if user_answer == quiz.answer1:
#         #     message = 'Correct answer!'
#         # else:
#         #     message = 'Incorrect answer, please try again.'
#     # else:
#     #     message = ''
#     context = {'quiz': quiz}
#     return render(request, 'quiz.html', context)
# def quiz_check(request,id):
#     quiz = quiz_answer.objects.get(id=id)
#     if request.method == 'POST':
#         user_answers = request.POST.getlist('answer')
#
#         total_marks = 0
#
#         for i, answer_id in enumerate(user_answers):
#             question = get_object_or_404(quiz_answer, id=i+1)
#             selected_answer = get_object_or_404(quiz_answer, id=int(answer_id))
#
#             if selected_answer.question == question and selected_answer.selected_answer == question.correct_answer:
#                 total_marks += 1
#
#         return render(request, 'quiz_result.html', {'total_marks': total_marks})
#
#     else:
#         questions = quiz_answer.objects.all()
#         return render(request, 'Quiz.html', {'questions': questions})

def add_coursematerials(request):
    if request.method == "POST":
        course  = request.POST.get('course')
        title = request.POST.get('title')
        file = request.FILES.get('file')
        coursematerial = Course_material(course=course, title=title, file=file)
        coursematerial.save()
        messages.info(request,'Course materials has been successfully uploaded..!!')
        return redirect('add_coursematerials')
    return render(request, 'Add_coursematerials.html')


# def add_coursematerial(request, course_id):
#     if request.method == 'POST':
#         course = Course.objects.get(id=course_id)
#         title = request.POST.get('title')
#         file = request.FILES.get('file')
#         course_material = CourseMaterial(course=course, title=title, file=file)
#         course_material.save()
#         messages.success(request, 'Course material added successfully!')
#         return redirect('mentor_dashboard')
#     else:
#         course = Course.objects.get(id=course_id)
#         return render(request, 'add_course_material.html', {'course': course})
# def add_coursematerials(request, id):
#     course = get_object_or_404(Course, id=id)
#
#     if request.method == 'POST':
#         title = request.POST['title']
#         file = request.FILES['file']
#         course_material = CourseMaterial(course=course, title=title, file=file)
#         course_material.save()
#         messages.success(request, 'Course material added successfully!')
#         return redirect('mentor_dashboard')
#
#     return render(request, 'add_course_materials.html', {'course': course})

import os
from django.http import HttpResponse, Http404
from django.conf import settings
from .models import Course_material

def download_course_material(request,file):
    course_material = Course_material.objects.get(file=file)
    file_path =os.path.join(settings.MEDIA_ROOT, 'coursematerials', str(course_material.file))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def job_details(request,id):
    job = Job.objects.get(id=id)
    context = {
        'job': job,
    }
    return render(request, "job-detail.html", context)
def job_apply(request):
    if request.method == "POST":
        applicant_name = request.POST.get('applicant_name')
        applicant_email = request.POST.get('applicant_email')
        resume = request.FILES.get('resume')
        apply_job = Apply_job(applicant_name=applicant_name, applicant_email=applicant_email, resume=resume)
        apply_job.save()
        messages.info(request, 'Job applied successfully..!!')
        return redirect('job_apply')
    return render(request, 'job-list.html')


def course_detail(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    point = what_you_learn.objects.all()
    req = requirements.objects.all()
    context = {
        'course': course,
        'results': point,
        'res': req,

    }
    return render(request, "course-single-v4.html", context)
def enroll_course(request, slug):
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=slug)
        user = request.user
        enrollment = Enrollment.objects.filter(user=user, course=course).exists()

        if enrollment:
            messages.warning(request, 'You are already enrolled in this course.')
        else:
            enrollment = Enrollment(user=user, course=course)
            enrollment.save()
            messages.success(request, 'You have successfully enrolled in the course!')

        return redirect('course_detail',slug)
    return render(request, 'course-single-v4.html')


def Course_materilals_view(request,id):
    if 'email' in request.session:
        email=request.session['email']
        data=Course_material.objects.get(id=id)
        context = {
            'data': data
        }
        return render(request, 'Learner/CourseMaterials.html', context)
    else:
        return redirect(Home)

def download_pdf_CM(request, id):
    pdf_file = get_object_or_404(Course_material, id=id)
    return FileResponse(pdf_file.file, as_attachment=True)

def quiz_answer(request,course_id):
    quiz = get_object_or_404(table_quiz, id=course_id)

    if request.method == 'POST':
        answer1 = request.POST.get('answer1')
        answer2 = request.POST.get('answer2')
        answer3 = request.POST.get('answer3')
        answer4 = request.POST.get('answer4')
        score = 0
        total = 40



        if answer1 == quiz.answer1:
            score += 10

        if answer2 == quiz.answer2:
            score += 10

        if answer3 == quiz.answer3:
            score += 10

        if answer4 == quiz.answer4:
            score += 10

        percent = score / (total) * 100

        QuizResult.objects.create(user=request.user, quiz=quiz, score=score, percent=percent )
        if percent >= 75:
            messages.success(request, 'Congratulations! You scored above 75% on the quiz and you can download your course certificate')
        else:
            messages.info(request, 'You scored below 75% on the quiz,Try again.. !!!!!')
        return render(request, 'result.html', {'score': score,'percent':percent,'timer':request.POST.get('timer')})

    return render(request, 'Quiz.html', {'quiz': quiz})

# def generate_certificate(request, id):
#     course = Course.objects.get(id=id)
#     certificate = Certificate.objects.all()
#     quiz_result = QuizResult.objects.all()
#
#     if quiz_result.percent >= 75:
#         certificate, created = Certificate.objects.get_or_create(user=request.user, quiz_result=quiz_result)
#         if created:
#          return render(request, 'certificate1.html', {'course': course, 'certificate': certificate})
#         else:
#          return render(request, 'error.html', {'message': 'You must complete the course to generate a certificate.'})


# def generate_certificate(request):
#     course = Course.objects.filter(id=1)
#     certificate = Certificate.objects.all()
#     # user_progress = Course.objects.get(course_name=course)
#     quizresult = QuizResult.objects.filter(user=request.user).first()
#     if quizresult.percent >= 75:
#         # generate certificate logic here
#         return render(request, 'certificate1.html', {'course': course, 'certificate': certificate})
#     else:
#         messages.info(request, 'Unable to  download certificate !!!!!')
#         # return render(request, 'Quiz.html', {'message': 'You must complete the course to generate a certificate.'})
#         return render(request, 'error-404.html')
# def generate_certificate(request, id):
#     course = Course.objects.get(id=id)
#     certificate = Certificate.objects.all()
#     user_progress = QuizResult.objects.filter(user=request.user).first()
#     if user_progress and user_progress.percent >= 75:
#         # generate certificate logic here
#         return render(request, 'certificate1.html', {'course': course, 'certificate': certificate})
#     else:
#         messages.info(request, 'You scored below 75% on the quiz,Try again.. !!!!!')
#
#         return render(request, 'Quiz.html', {'message': 'You must complete the course and achieve a percentage of 75 or higher to generate a certificate. Please try again.'})


def download_pdf_Certificate(request, id):
    pdf_file = get_object_or_404(Certificate, id=id)
    return FileResponse(pdf_file.certificate_image, as_attachment=True)