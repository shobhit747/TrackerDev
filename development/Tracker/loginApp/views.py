from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from .models import Organization
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail

# Create your views here.

def registrationView(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = str(email).lower()
        password = request.POST['password']
        try:

            newUser = User.objects.create_user(username,email,password)
            newUser.save()
            user = User.objects.get(email = email)
            Organization.objects.create(user = user,organizationName = request.POST['orgName'])
            loginUser = authenticate(request, username=username, password=password)

            if loginUser is not None:
                login(request, loginUser)
            else:
                print('do not exist')
        except:
            print('user already exist')

    # if user is logged in go to dashboard instead of registration 
    if request.user.is_authenticated:
        return redirect("staticsView")
    
    return render(request,'Registration.html')

@login_required
def registrationOrgInfoView(request):
    request.session.set_expiry(0)
    user = request.user
    org = Organization.objects.get(user = user)
    
    if request.method == 'POST':
        org.localAddress = request.POST['localAddress']
        org.aboutOrg = request.POST['orgDiscription']
        org.save()
        if org.mobile == 'none':
            return redirect('registrationSendOtpView')
        else:
            return redirect('staticsView')
    temp = {
        'orgName':org.organizationName,
    }
    return render(request,'RegistrationOrgInfo.html',temp)

@login_required
def registrationSendOtpView(request):
    request.session.set_expiry(0)
    user = request.user
    org = Organization.objects.get(user = user)

    if request.method == 'POST':
        mobileNumber = request.POST['mobileNumber']
        otp = random.randint(1000,9999)
        request.session['otp'] = [mobileNumber,otp]
        send_mail(
            'Your OTP',otp,'shobhitthakur70@gmail.com',['anurag83191@gmail.com'],fail_silently=False
        )
        return redirect('registrationReceiveOtpView')

    temp = {
        'orgName':org.organizationName,
    }
    return render(request,'RegistrationSendOtp.html',temp)

@login_required
def registrationReceiveOtpView(request):
    user = request.user
    org = Organization.objects.get(user = user)
    print(request.session['otp'])

    if request.method == 'POST':
        if int(request.POST['otp']) == request.session['otp'][1]:
            print('yesss',request.session['otp'][1])
            del request.session['otp']

        else:
            print('noooo')
    temp = {
        'orgName':org.organizationName,
    }
    return render(request,'RegistrationReceiveOtp.html',temp)

def loginView(request):
    if request.method == 'POST':
        username = str(request.POST['email']).lower()
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            print('do not exist')

    # if user is logged in go to dashboard instead of login 
    if request.user.is_authenticated:
        return redirect("staticsView")
    return render(request,'login.html')

def logoutView(request):
    logout(request)
    return redirect("loginView")
