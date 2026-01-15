from cloudinary.models import CloudinaryField
from django.shortcuts import get_object_or_404
from datetime import timezone
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    User profile with health and dietary information
    """
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )
    height_cm = models.FloatField(
        null=True, blank=True, help_text="Height in centimeters")
    weight_kg = models.FloatField(
        null=True, blank=True, help_text="Weight in kilograms")
    daily_calorie_goal = models.FloatField(
        null=True,
        blank=True,
        help_text="Daily calorie target"
    )
    bmi = models.FloatField(
        null=True,
        blank=True,
        help_text="Body Mass Index"
    )

    # In UserProfile model, add:
    meal_plan = models.ForeignKey(
        'MealPlan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_profile'
    )
    # Timestamps - ADD default=timezone.now
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True)      # Use auto_now for updates

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def calculate_bmi(self):
        """Calculate and update BMI"""
        if self. height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            self.bmi = round(self.weight_kg / (height_m ** 2), 2)
            return self.bmi
        return None

    def calculate_daily_calorie_needs(self):
        """Calculate daily calorie needs based on Mifflin-St Jeor Equation"""
        if not self.age or not self.weight_kg or not self.height_cm:
            return None

        if self.gender == 'male':
            bmr = 10 * self. weight_kg + 6.25 * self.height_cm - 5 * self.age + 5
        else:
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self. age - 161

        activity_factor = 1.2  # Sedentary
        self.daily_calorie_goal = round(bmr * activity_factor, 2)
        return self.daily_calorie_goal

    def save(self, *args, **kwargs):
        """Auto-calculate BMI and calorie goal before saving"""
        if self.height_cm and self.weight_kg:
            self.calculate_bmi()
        if self.age and self.weight_kg and self.height_cm:
            self.calculate_daily_calorie_needs()
        super().save(*args, **kwargs)


# Recipe Model
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
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes', default=1
    )

   # Timestamps - ADD default=timezone.now
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True)      # Use auto_now for updates

    class Meta:
        db_table = 'recipe'
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} {self.description}"

    def total_time(self):
        """Calculate total time"""
        return self.prep_time_minutes + self.cook_time_minutes


def save(self, *args, **kwargs):
    """Override save to ensure data integrity"""
    if self.servings <= 0:
        self.servings = 1
    if self.created_by is None:
        raise ValueError("Recipe must have a creator.")
    if self.created_at is None:
        self.created_at = timezone.now()
    super().save(*args, **kwargs)


# MealPlan Model
class MealPlan(models.Model):
    """
    User's meal plan with one recipe for each meal category
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meal_plans'
    )
    day = models.DateField(help_text="Date for this meal plan")
    # One recipe for each category
    breakfast_recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='meal_plan_breakfast'
    )
    lunch_recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='meal_plan_lunch'
    )
    dinner_recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='meal_plan_dinner'
    )
    snack_recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='meal_plan_snack'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'meal_plan'
        verbose_name = 'Meal Plan'
        verbose_name_plural = 'Meal Plans'
        unique_together = ['user', 'day']  # ADD THIS
        ordering = ['-day']  # ADD THIS - show newest first

    def __str__(self):
        return f"{self.user.username} - {self.day}"

    def get_total_calories(self):
        """Calculate total calories for the day"""
        total = 0
        for recipe in [self.breakfast_recipe, self.lunch_recipe,
                       self.dinner_recipe, self.snack_recipe]:
            if recipe:
                total += recipe.total_calories
        return total


def get_all_recipes(self, day):
    """Get all recipes as a dictionary"""
    return {
        'breakfast': self.breakfast_recipe,
        'lunch': self.lunch_recipe,
        'dinner': self.dinner_recipe,
        'snack': self.snack_recipe,
    }
