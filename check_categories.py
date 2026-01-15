from mealapp.models import Recipe
import os
import sys
import django
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planner.settings')
django.setup()


recipes = Recipe.objects.all()
categories = {}
for r in recipes:
    if r.category not in categories:
        categories[r.category] = 0
    categories[r.category] += 1

print(f'Total recipes: {recipes.count()}')
print(f'All categories: {categories}')
print()
for cat in ['breakfast', 'lunch', 'dinner', 'snack']:
    count = Recipe.objects.filter(category=cat).count()
    print(f'  {cat}: {count}')
