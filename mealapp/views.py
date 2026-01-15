from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from . models import Recipe, UserProfile
import json


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
    # This allows client-side category filtering across the entire dataset
    recipes_data = []
    for recipe in all_recipes:
        try:
            recipes_data.append({
                'id': recipe.id,
                'recipe_name': recipe.title,  # Match the new design's field name
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

    # Pagination - 12 recipes per page (for display purposes only)
    paginator = Paginator(all_recipes, 12)
    page_obj = paginator.get_page(page_number)

    print(f"DEBUG: Total recipes in DB: {all_recipes.count()}")
    print(f"DEBUG: Recipes on this page: {len(page_obj)}")
    print(f"DEBUG: Serialized recipes: {len(recipes_data)}")
    print(f"DEBUG: Page {page_obj.number} of {page_obj.paginator.num_pages}")

    context = {
        'recipes': page_obj,
        'recipes_json': json.dumps(recipes_data),
        'search_term': search,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
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

    return render(request, 'mealapp/dashboard.html', context)
