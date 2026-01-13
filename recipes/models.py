from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from cloudinary.models import CloudinaryField
# Create your models here.

# Create your models here.


class Recipe(models.Model):
    """
    Docstring for Recipe
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()
    image_url = CloudinaryField('image', default='placeholder')
    servings = models.IntegerField(default=1)
    prep_time_minutes = models.IntegerField(default=0)
    cook_time_minutes = models.IntegerField(default=0)
    ingredients = models.JSONField()
    # List of ingredients with quantities
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    total_calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    category = models.CharField(max_length=20, choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ])


class Meta:
    db_table = 'recipe'


def __str__(self):
    return self.title
