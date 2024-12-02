from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .userDataFuncs.userData import hauth2

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        try:
            if hauth2(username, password):
                return redirect(reverse('dashboard'))  
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password'})
        except ValueError as e:
            return render(request, 'login.html', {'error': str(e)})

    return render(request, 'login.html')

def dashboard_view(request):
    pass #do this later #comment
