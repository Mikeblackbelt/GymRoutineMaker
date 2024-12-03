import json
import .userDataFuncs.userData as UDF
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

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
    pass #do this later 

def emailVerify_view(request):
    pas