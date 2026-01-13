from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from cloudinary.models import CloudinaryField
# Create your models here.

# Create your models here.


class Recipe(models.Model):
    """
    Recipe model with ingredients and nutrition info
    """
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    # Basic Info
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()
    image_url = CloudinaryField('image', default='placeholder')

    # Servings and Time
    servings = models.IntegerField(default=1)
    prep_time_minutes = models.IntegerField(default=0)
    cook_time_minutes = models.IntegerField(default=0)

    # Ingredients (stored as JSON)
    ingredients = models.JSONField(
        help_text="List of ingredients with quantities"
    )

    # Nutrition Info
    total_calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()

    # Category
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    # Ownership
    created_by = models. ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    # Timestamps
    created_at = models.DateTimeField(timezone)
    updated_at = models.DateTimeField(timezone)

    class Meta:
        db_table = 'recipe'
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def total_time(self):
        """Calculate total time"""
        return self.prep_time_minutes + self.cook_time_minutes
