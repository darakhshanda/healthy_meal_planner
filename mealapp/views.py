from multiprocessing import context
from unicodedata import category
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from requests import request
from mealapp.forms import MealPlanForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, date
from .models import MealPlan, Recipe, UserProfile
from .forms import ProfileSetupForm, MealPlanForm, RecipeForm, IngredientInlineForm
from os import path
import json
# Home & Index


def index(request):
    search = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)

    # Get all recipes
    all_recipes = Recipe.objects.all()

    if search:
        all_recipes = all_recipes.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    # Serialize ALL recipes manually to handle JSONField and CloudinaryField
    recipes_data = []
    for recipe in all_recipes:
        try:
            recipes_data.append({
                'id': recipe.id,
                'recipe_name': recipe.title,
                'category': recipe.category,
                'description': recipe.description,
                'ingredients': recipe.ingredients if isinstance(recipe.ingredients, list) else [],
                'instructions': recipe.instructions.split('\n') if recipe.instructions else [],
                'image_url': recipe.image_url.url if hasattr(recipe.image_url, 'url') else str(recipe.image_url),
                'prep_time_minutes': recipe.prep_time_minutes,
                'total_calories': recipe.total_calories,
                'servings': recipe.servings,
                'protein': recipe.protein,
                'carbs': recipe.carbs,
                'fat': recipe.fat,
            })
        except Exception as e:
            print(f"Error serializing recipe {recipe.id}: {e}")
            continue

    # Pagination - 12 recipes per page
    paginator = Paginator(all_recipes, 12)
    page_obj = paginator.get_page(page_number)

    context = {
        'recipes': page_obj,
        'recipes_json': json.dumps(recipes_data),
        'search_term': search,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'mealapp/index.html', context)


# Profile Setup
@login_required()
def profile_setup(request):
    """User profile setup/edit view"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            # copy fields to user model
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.age = form.cleaned_data.get('age')
            profile.gender = form.cleaned_data.get('gender')
            profile.height_cm = form.cleaned_data.get('height_cm')
            profile.weight_kg = form.cleaned_data.get('weight_kg')
            profile.daily_calorie_goal = form.cleaned_data.get(
                'daily_calorie_goal')
            profile.bmi = form.cleaned_data.get('bmi')

            profile.save()
            messages.success(
                request, f'✅ Profile saved! Your BMI is {profile.bmi} and daily calorie goal is {profile.daily_calorie_goal} kcal.')
            messages.info(
                request, 'You can now start creating meal plans and adding recipes.')
            return redirect('dashboard')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = ProfileSetupForm(instance=profile)

    return render(request, 'mealapp/profile_setup.html', {
        'form': form,
        'profile': profile
    })


# Dashboard
@login_required(login_url='account_login')
def dashboard(request):
    """User dashboard view showing meal plans and progress"""
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user)

    # Get today's meal plan
    today = date.today()
    meal_plan, created = MealPlan.objects.get_or_create(
        user=request.user,
        day=today
    )

    # Get user's recipes count
    user_recipes_count = Recipe.objects.filter(created_by=request.user).count()

    # Calculate remaining calories
    total_calories = meal_plan.get_total_calories()
    remaining_calories = (
        user_profile.daily_calorie_goal or 0) - total_calories

    context = {
        'user_profile': user_profile,
        'meal_plan': meal_plan,
        'today': today,
        'total_calories': total_calories,
        'remaining_calories': remaining_calories,
        'user_recipes_count': user_recipes_count,
    }
    return render(request, 'mealapp/dashboard.html', context)


# Meal Plan CRUD
@login_required
def meal_plan_list_view(request):
    """List all meal plans for the user, sorted by date (newest first)"""
    meal_plans = MealPlan.objects.filter(user=request.user).order_by('-day')

    context = {
        'meal_plans': meal_plans,
        'is_list_view': True,
    }
    return render(request, 'mealapp/meal_plan.html', context)


@login_required
def meal_plan_current(request):
    """Redirect to today's meal plan"""
    today = date.today()
    return redirect('meal_plan_view', date=today.strftime('%Y-%m-%d'))


@login_required
def create_meal_plan(request):
    """Redirect to meal plan list where users can select a date"""
    return redirect('meal_plan_list')


@login_required
def meal_plan_view(request, date):
    """View/Edit meal plan for a specific date"""
    try:
        parsed_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return redirect('dashboard')

    meal_plan, created = MealPlan.objects.get_or_create(
        user=request.user,
        day=parsed_date
    )
    recipes = Recipe.objects.all().order_by('category', 'title')

    if request.method == 'POST':
        meal_plan.breakfast_recipe_id = request.POST.get('breakfast')
        meal_plan.lunch_recipe_id = request.POST.get('lunch')
        meal_plan.dinner_recipe_id = request.POST.get('dinner')
        meal_plan.snack_recipe_id = request.POST.get('snack')
        meal_plan.save()
        messages.success(request, 'Meal plan updated successfully!')
        return redirect('dashboard')

    return render(request, 'mealapp/meal_plan.html', {
        'meal_plan': meal_plan,
        'recipes': recipes,
        'date': parsed_date,
    })


@login_required
def meal_plan_update(request, plan_id):
    """Update a specific meal plan"""
    meal_plan = get_object_or_404(MealPlan, id=plan_id, user=request.user)
    recipes = Recipe.objects.all().order_by('category', 'title')

    if request.method == 'POST':
        meal_plan.breakfast_recipe_id = request.POST.get('breakfast')
        meal_plan.lunch_recipe_id = request.POST.get('lunch')
        meal_plan.dinner_recipe_id = request.POST.get('dinner')
        meal_plan.snack_recipe_id = request.POST.get('snack')
        meal_plan.save()
        messages.success(request, 'Meal plan updated successfully!')
        return redirect('dashboard')

    return render(request, 'mealapp/meal_plan.html', {
        'meal_plan': meal_plan,
        'recipes': recipes,
        'date': meal_plan.day,
    })


@login_required
def delete_meal_plan(request, plan_id):
    """Delete a specific meal plan"""
    meal_plan = get_object_or_404(MealPlan, id=plan_id, user=request.user)

    if request.method == 'POST':
        meal_plan.delete()
        messages.success(request, 'Meal plan deleted successfully!')
        return redirect('meal_plan_list')

    # Adds a success message upon deletion
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Meal plan deleted successfully!')
        return super().delete(request, *args, **kwargs)

    # GET request - show confirmation
    recipes = Recipe.objects.all().order_by('category', 'title')
    return render(request, 'mealapp/meal_plan.html', {
        'meal_plan': meal_plan,
        'recipes': recipes,
        'date': meal_plan.day,
        'confirm_delete': True,
    })


# Recipe CRUD
# Recipe Detail to show single recipe
def recipe_detail(request, recipe_id):
    """View for displaying a single recipe's details"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context = {
        'recipe': recipe,
        'ingredients': recipe.ingredients if isinstance(recipe.ingredients, list) else [recipe.ingredients]
    }

    return render(request, 'mealapp/recipe_detail.html', context)


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'mealapp/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12

    def get_queryset(self):
        queryset = Recipe.objects.filter(
            created_by=self.request.user).order_by('-created_at')
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category'] = self.request.GET.get('category', '')
        return context


def recipe_list_user(request, username):
    """List recipes created by a specific user"""
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(created_by=user).order_by('-created_at')

    context = {
        'recipes': recipes,
        'created_by': user,
    }
    return render(request, 'mealapp/recipe_list.html', context)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'mealapp/recipe_create.html'
    fields = ['title', 'description', 'instructions', 'image_url',
              'servings', 'prep_time_minutes', 'cook_time_minutes',
              'ingredients', 'total_calories', 'protein', 'carbs', 'fat', 'fiber', 'category']
    success_url = reverse_lazy('recipe_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Recipe created successfully!')
        return super().form_valid(form)


@login_required
def recipe_edit_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, created_by=request.user)

    if request.method == 'POST':
        initial_ingredients = recipe.ingredients if isinstance(
            recipe.ingredients, list) else []
        total_forms = request.POST.get('form-TOTAL_FORMS', 0)
        for i in range(int(total_forms)):
            if not request.POST.get(f'form-{i}-DELETE'):
                initial_ingredients.append({
                    'name': request.POST.get(f'form-{i}-name', ''),
                    'quantity': request.POST.get(f'form-{i}-quantity', ''),
                    'unit': request.POST.get(f'form-{i}-unit', ''),
                })
        form = RecipeForm(request.POST, instance=recipe,
                          initial_ingredients=initial_ingredients)
        if form.is_valid():
            form.save(created_by=request.user)
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm(
            instance=recipe, initial_ingredients=recipe.ingredients or [])

    return render(request, 'mealapp/recipe_create.html', {
        'form': form,
        'recipe': recipe,
    })


def recipe_detail(request, pk):
    """Display single recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


@login_required
def recipe_delete(request, pk):
    """Delete recipe"""
    recipe = get_object_or_404(Recipe, pk=pk, created_by=request.user)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully!')
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


@login_required
def recipeCreateView(request):
    if request.method == 'POST':
        initial_ingredients = []
        total_forms = request.POST.get('form-TOTAL_FORMS', 0)
        for i in range(int(total_forms)):
            if not request.POST.get(f'form-{i}-DELETE'):
                initial_ingredients.append({
                    'name': request.POST.get(f'form-{i}-name', ''),
                    'quantity': request.POST.get(f'form-{i}-quantity', ''),
                    'unit': request.POST.get(f'form-{i}-unit', ''),
                })
        form = RecipeForm(
            request.POST, initial_ingredients=initial_ingredients)
        if form.is_valid():
            recipe = form.save(created_by=request.user)
            messages.success(request, 'Recipe created successfully!')
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()

    return render(request, 'mealapp/recipe_create.html', {'form': form})


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = 'mealapp/recipe_create.html'
    fields = ['title', 'description', 'instructions', 'image_url',
              'servings', 'prep_time_minutes', 'cook_time_minutes',
              'ingredients', 'total_calories', 'protein', 'carbs', 'fat', 'fiber', 'category']
    success_url = reverse_lazy('recipe_list')

    def get_queryset(self):
        return Recipe.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Recipe updated successfully!')
        return super().form_valid(form)


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'mealapp/recipe_confirm_delete.html'

    # Limit deletion to recipes created by the logged-in user
    def get_queryset(self):
        return Recipe.objects.filter(created_by=self.request.user)
    # Redirect to the user's recipe list after deletion

    def get_success_url(self):
        return reverse_lazy('recipe_list_user', kwargs={'username': self.request.user.username})

    # Adds a success message upon deletion
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Recipe deleted successfully!')
        return super().delete(request, *args, **kwargs)


def help_page(request):
    """Help page"""
    return render(request, 'mealapp/help.html', {'title': 'Help'})
