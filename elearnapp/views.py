from hashlib import sha256

from django.contrib import messages
from django.shortcuts import render, redirect


from elearnapp.models import user_reg, user_log, freecourses, paidcourses, pyintro, pyadva, javaintro, javaadva


# Create your views here.


def demo(request):
    return render(request,"index.html")


def home1(request):
    return render(request,"index.html")


def home2(request):
    return render(request,"index-2.html")


def LOGIN(request):
    return render(request,"LOGIN.html")


def REGISTRATION(request):
    return render(request, "REGISTRATION.html")


def Home(request):
    return render(request,"Home.html")


def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        state = request.POST['state']
        country = request.POST['country']
        paswd = sha256(password.encode()).hexdigest()
        user = user_reg(name=name,email=email,password=paswd,phone=phone,address=address,state=state,country=country)
        log = user_log(email=email,password=paswd)
        user.save()
        log.save()
        messages.info(request, 'Your account has been successfully created..!!')
        return redirect('LOGIN')
    return render(request, 'REGISTRATION.html')

# Login Function


def login(request):
    request.session.flush()
    if 'email' in request.session:
        return redirect(home)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = sha256(password.encode()).hexdigest()
        user = user_log.objects.filter(email=email,password=password2)
        if user:
            user_details = user_log.objects.get(email=email,password=password2)
            email = user_details.email
            request.session['email'] = email
            return redirect('home')
        else:
            print("Invalid")
    return render(request,'LOGIN.html')


def home(request):
    if 'email' in request.session:
        email = request.session['email']
        return render(request,'Home.html',{'email':email})
    return redirect(login)


def about1(request):
    return render(request,"about-1.html")


def about2(request):
    return render(request,"about-2.html")


def userprofile(request):
    return render(request,"user-profile.html")


def dashboard(request):
    return render(request,"index_admin.html")


def reports(request):
    return render(request,"Reports.html")


def activity(request):
    return render(request,"list-view-calendar.html")


def Messages(request):
    return render(request,"mailbox.html")


def course(request):
    return render(request,"paid courses.html")


def coursesdetails(request):
    obj=pyintro.objects.all()
    return render(request,"courses-details.html",{'result':obj})


def coursesdetailsp2(request):
    obj=pyadva.objects.all()
    return render(request,"courses-details p2.html",{'result':obj})


def javaintrod(request):
    obj=javaintro.objects.all()
    return render(request,"java1.html",{'result':obj})


def javaadv(request):
    obj=javaadva.objects.all()
    return render(request,"java1.html",{'result':obj})


def freecourse(request):
    obj = freecourses.objects.all()
    return render(request,"free courses.html",{'result':obj})


def paidcourse(request):
    obj = paidcourses.objects.all()
    return render(request,"paid courses.html",{'result':obj})

