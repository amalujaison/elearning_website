from django.shortcuts import render
from django.contrib import auth, messages
from django.shortcuts import redirect, render

from elearningapp.models import Account
# Create your views here.


def demo(request):
    return render(request,"index.html")


def LOGIN(request):
    return render(request,"LOGIN.html")

def REGISTRATION(request):
    return render(request, "REGISTRATION.html")
#



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pswd = request.POST.get('pass')
        print(email, pswd)
        user = auth.authenticate(email=email, password=pswd)
        print(user)

        if user is not None:
            auth.login(request, user)
            # save email in session
            request.session['email'] = email

            if user.is_admin:
                return redirect('admin/')

            else:
                return redirect('User_Home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'login.html')


def user_reg(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
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
        user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, phone=phone, address=address, state=state, country=country,
                                           password=password)
        user.is_user = True
        user.save()
        messages.info(request, 'Thank you for registering with us. Please Login')
        return redirect('LOGIN')
    return render(request, 'REGISTRATION.html')


def logout(request):
    auth.logout(request)
    return redirect('User_Home')

