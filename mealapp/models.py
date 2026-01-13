from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """User profile with health and dietary information"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField()
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
    )
    height_cm = models.FloatField(help_text="Height in centimeters")
    weight_kg = models.FloatField(help_text="Weight in kilograms")

    daily_calorie_goal = models.FloatField(
        null=True, blank=True, help_text="Daily calorie target")
    bmi = models.FloatField(null=True, blank=True, help_text="Body Mass Index")

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def calculate_bmi(self):
        """Calculate and update BMI"""
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            self.bmi = round(self.weight_kg / (height_m ** 2), 2)
            return self.bmi
        return None

    def set_daily_calorie_goal(self, goal):
        """Set daily calorie goal"""
        self.daily_calorie_goal = goal
        self.save()

    def calculate_daily_calorie_needs(self):
        """Calculate daily calorie needs based on Mifflin-St Jeor Equation"""
        if self.gender == 'male':
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age + 5
        else:
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age - 161
        activity_factor = 1.2  # Sedentary
        daily_calories = bmr * activity_factor
        return daily_calories


class Admin(models.Model):
    """Admin profile extending auth_user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipe_created = models.CharField(
        max_length=255, blank=True, null=True, help_text="Admin permissions or role")

    class Meta:
        db_table = 'admin'

    def __str__(self):
        return f"Admin: {self.user.username}"
