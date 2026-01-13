from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.


def main_page(request):
    """Main landing page"""
    return render(request, 'index.html')


def register_view(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Passwords do not match")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')
