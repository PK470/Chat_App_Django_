from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .form import UserRegistrationForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def user_login(request):
    """User Login"""
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=user, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
    else:
        form = UserLoginForm()
    return render(request,'login.html',{'form':form})


def user_register(request):
    """User Register"""
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration Successful')
            return redirect('login')
        else:
            messages.error(request,'Something went wrong!')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html',{'form':form})

def user_logout(request):
    """User Logout"""
    logout(request)
    return redirect('login')
  