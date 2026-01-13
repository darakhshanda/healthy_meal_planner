from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.


def main_page(request):
    """Main landing page"""
    return render(request, 'mealapp/index.html')
# ==================== Authentication Views ====================


def register_view(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Validation
        if password != password_confirm:
            messages.error(request, "Passwords do not match")
            return render(request, 'users/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'users/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'users/register.html')

        # Create user and profile
        user = User.objects.create_user(
            username=username, email=email, password=password)
        UserProfile.objects.create(user=user)

        messages.success(
            request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'users/register.html')


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'mealapp/login.html')


@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('main_page')


# ==================== Profile Views ====================

@login_required
def profile_edit_view(request):
    """Edit user profile"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update user info
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()

        # Update profile info
        profile.age = request.POST.get('age') or None
        profile.gender = request.POST.get('gender') or None
        profile.height_cm = request.POST.get('height_cm') or None
        profile.weight_kg = request.POST.get('weight_kg') or None
        profile.activity_level = request.POST.get('activity_level', 'moderate')

        # Calculate BMI and calorie goal
        if profile.height_cm and profile.weight_kg:
            profile.calculate_bmi()

        if all([profile.age, profile.weight_kg, profile.height_cm, profile.gender]):
            profile.calculate_calorie_goal()
        else:
            # Manual calorie goal if auto-calculation not possible
            manual_goal = request.POST.get('daily_calorie_goal')
            if manual_goal:
                profile.daily_calorie_goal = float(manual_goal)

        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    context = {
        'profile': profile
    }

    return render(request, 'mealapp/profile_edit.html', context)


@login_required
def dashboard_view(request):
    """User dashboard"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Check if profile is incomplete
    profile_complete = all([
        profile.age,
        profile.gender,
        profile.height_cm,
        profile.weight_kg,
        profile.daily_calorie_goal
    ])

    context = {
        'profile': profile,
        'profile_complete': profile_complete
    }

    return render(request, 'users/dashboard.html', context)
# Recipe Views


@login_required
def recipe_list_view(request):
    """View to list all recipes"""
    recipes = Recipe.objects.all().order_by('-category', 'title')

    search_query = request.GET.get('search', '')
    if search_query:
        recipes = recipes.filter(Q(title__icontains=search_query) | Q(
            description__icontains=search_query))

    category = request.GET.get('category', '')
    if category:
        recipes = recipes.filter(category__iexact=category)
    context = {
        'recipes': recipes,
        'search_query': search_query,
        'selected_category': category,
        'categories': ['breakfast', 'lunch', 'dinner', 'snack']
    }
    return render(request, 'recipes/recipe_list.html', context)
