from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import *

# Create your views here.

def register_request(request):
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request,'User with this email already exists, Use a different email!!')
                return redirect('register')
            else:
                user = form.save()
                login(request, user)
                # messages.success(request, "Successful Registered!")
                return redirect('home')
    else:
        form = registerForm()
    context = {
        'form':form
    }
    return render(request, 'userauth/register.html', context)


def login_request(request):
    if request.method == 'POST':
        form = loginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                   return redirect(request.POST.get('next'))
                return redirect('home')
        else:
            messages.error(request, "Username or Password is Incorrect")
            redirect('login')
    else:
        form = loginForm()
    context = {
        'form':form
    }
    return render(request, 'userauth/login.html', context)



def logout_request(request):
    logout(request)
    messages.success(request,f"Logged out successful")
    return redirect('login')