import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .userDataFuncs import userData as UDF

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        try:
            if UDF.hauth2(username, password):
                userdata = UDF.getUserData(username = username)
                return redirect(reverse('dashboard')) if not userdata['settings']['2auth'] else redirect(reverse('emailVerify'))
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})
        except ValueError as e:
            return render(request, 'login.html', {'error': str(e)})

    return render(request, 'login.html')

def dashboard_view(request):
    pass #do this later #comment

def signup_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        try:
            new_user = UDF.User(name=name, username=username, password=password, email=email)
            new_user.upload()
            return redirect('login')  # Redirect to login after successful sign-up
        except Exception as e:
            return render(request, 'signup.html', {"error": str(e)})

    return render(request, 'signup.html')

def emailVerify_view(request):
    pass