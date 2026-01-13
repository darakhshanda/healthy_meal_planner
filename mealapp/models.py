from time import timezone
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
    age = models.IntegerField()
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )
    height_cm = models.FloatField(help_text="Height in centimeters")
    weight_kg = models.FloatField(help_text="Weight in kilograms")
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

    # Timestamps
    created_at = models.DateTimeField(timezone)
    updated_at = models.DateTimeField(timezone)

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
