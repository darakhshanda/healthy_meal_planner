from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .models import Recipe
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.


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
