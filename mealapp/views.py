from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . models import Recipe, UserProfile


def index(request):
    """Home page view"""

    # Get search term
    search = request.GET.get('search', )

    # Get recipes by category (3 per category for wireframe layout)
    breakfast_recipes = Recipe.objects.filter(category='breakfast')[:3]
    lunch_recipes = Recipe.objects.filter(category='lunch')[:3]
    dinner_recipes = Recipe.objects.filter(category='dinner')[:3]
    snack_recipes = Recipe.objects.filter(category='snack')[:3]

    # Apply search if provided
    if search:
        breakfast_recipes = breakfast_recipes.filter(title__icontains=search)
        lunch_recipes = lunch_recipes.filter(title__icontains=search)
        dinner_recipes = dinner_recipes.filter(title__icontains=search)
        snack_recipes = snack_recipes.filter(title__icontains=search)

    context = {
        'search_term': search,
        'breakfast_recipes': breakfast_recipes,
        'lunch_recipes': lunch_recipes,
        'dinner_recipes': dinner_recipes,
        'snack_recipes': snack_recipes,
    }

    return render(request, 'mealapp/index.html', context)


def recipe_detail(request, recipe_id):
    """View for displaying a single recipe's details"""

    # Fetch the recipe or return 404
    recipe = get_object_or_404(Recipe, id=recipe_id)

    context = {
        'recipe': recipe,
    }

    return render(request, 'mealapp/recipe_detail.html', context)


@login_required
def dashboard(request):
    """User dashboard view showing meal plans and progress"""

    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user)
    # meal_plans = user_profile.mealplan_set.all()

    context = {
        'user_profile': user_profile,
        # 'meal_plans': meal_plans,
    }

    return render(request, 'dashboard.html', context)
