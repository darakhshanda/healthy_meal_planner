from datetime import date, datetime
import json
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, HTML
from django.forms import formset_factory
from django.urls import reverse
from .models import MealPlan, UserProfile, Recipe
from mealapp import models
import re


class ProfileSetupForm(forms.ModelForm):
    """Form for setting up user profile"""

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'age',
                  'weight_kg', 'height_cm', 'gender', 'user_image']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Enter your full name'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Enter your full name'}),
            'age': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 0,
                       'placeholder': 'Enter your age'}),
            'weight_kg': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 0,
                       'placeholder': 'Enter your weight (kg)'}),
            'height_cm': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 0,
                       'placeholder': 'Enter your height (cm)'}),
        }

        labels = {
            'age': 'Age (years)',
            'gender': 'Gender',
            'height_cm': 'Height (cm)',
            'weight_kg': 'Weight (kg)',

        }

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        height_cm = cleaned_data.get('height_cm')
        weight_kg = cleaned_data.get('weight_kg')

        # Validate age
        if age and (age < 1 or age > 150):
            self.add_error('age', 'Age must be between 1 and 150.')

        # Validate height
        if height_cm and (height_cm < 50 or height_cm > 300):
            self.add_error(
                'height_cm', 'Height must be between 50 and 300 cm.')

        # Validate weight
        if weight_kg and (weight_kg < 10 or weight_kg > 500):
            self.add_error(
                'weight_kg', 'Weight must be between 10 and 500 kg.')

    def save(self, commit=True):
        """Save profile and update user name"""
        user = self.instance.user
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')

        user.save()

        return super().save(commit=commit)


class MealPlanForm(forms.ModelForm):
    """Simplified meal plan form"""

    class Meta:
        model = MealPlan
        fields = ['day', 'breakfast_recipe',
                  'lunch_recipe', 'dinner_recipe', 'snack_recipe']
        widgets = {
            'day': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-lg',
                'min': datetime.date,
            }),
        }
        labels = {
            'day': 'Select Day',
        }
        help_texts = {
            'day': 'Choose the day for your meal plan',
        }

    def clean_day(self):
        day = self.cleaned_data.get('day')
        # Must be a Monday
        if day and day.weekday() != 0:
            raise forms.ValidationError("Week must start on Monday.")

        # Cannot be in the past
        if day and day < date.today():
            raise forms.ValidationError("Week cannot start in the past.")

        return day


class MealSelectionForm(forms.Form):
    """Form for selecting a single meal"""
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    day = forms.ChoiceField(
        choices=[
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
            ('sunday', 'Sunday'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    meal_type = forms.ChoiceField(
        choices=[
            ('breakfast', 'Breakfast'),
            ('lunch', 'Lunch'),
            ('dinner', 'Dinner'),
            ('snack', 'Snack'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    recipe = forms.ModelChoiceField(
        queryset=Recipe.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="-- Select Recipe --"
    )

    def __init__(self, *args, **kwargs):
        meal_type = kwargs.pop('meal_type', None)
        super().__init__(*args, **kwargs)

        # Filter recipes by meal type
        if meal_type:
            self.fields['recipe'].queryset = Recipe.objects.filter(
                category=meal_type
            )
        # Filter recipes by user or show all public recipes
        if User:
            # Show user's recipes + public recipes
            self.fields['breakfast'].queryset = Recipe.objects.filter(
                category='breakfast'
            ).filter(
                created_by=User
            ) | Recipe.objects.filter(category='breakfast', is_public=True)

            self.fields['lunch'].queryset = Recipe.objects.filter(
                category='lunch'
            ).filter(
                created_by=User
            ) | Recipe.objects.filter(category='lunch', is_public=True)
            self.fields['dinner'].queryset = Recipe.objects.filter(
                category='dinner'
            ).filter(
                created_by=User
            ) | Recipe.objects.filter(category='dinner', is_public=True)
            self.fields['snack'].queryset = Recipe.objects.filter(
                category='snack'
            ).filter(
                created_by=User
            ) | Recipe.objects.filter(category='snack', is_public=True)


class RecipeForm(forms.ModelForm):
    """Form for creating and editing recipes"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate ingredients_text
        # and instructions_text for textarea fields
        if self.instance and self.instance.pk:
            # Ingredients
            ingredients = self.instance.ingredients
            if isinstance(ingredients, list):
                self.initial['ingredients_text'] = '\n'.join(ingredients)
            elif isinstance(ingredients, str):
                self.initial['ingredients_text'] = ingredients
            else:
                self.initial['ingredients_text'] = ''
            # Instructions
            instructions = self.instance.instructions
            if isinstance(instructions, list):
                self.initial['instructions_text'] = '\n'.join(instructions)
            elif isinstance(instructions, str):
                self.initial['instructions_text'] = instructions
            else:
                self.initial['instructions_text'] = ''

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'prep_time_minutes',
            'cook_time_minutes', 'servings', 'image_url',
            'category', 'total_calories', 'carbs', 'protein',
            'fat', 'fiber',
        ]
        excludes = ['created_by', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 2, 'cols': 40, 'class': 'form-control'}),
            'image_url': forms.ClearableFileInput(
                attrs={'class': 'form-control'}),
        }

    # Validation for ingredients and instructions
    def clean(self):
        cleaned_data = super().clean()
        raw_ingredients = self.data.get('ingredients_text', '')
        import re
        raw_ingredients = re.sub(r"[\[\]\'\"]", '', raw_ingredients)
        if '\n' in raw_ingredients:
            ingredients = [i.strip()
                           for i in raw_ingredients.split('\n') if i.strip()]
        else:
            ingredients = [i.strip()
                           for i in raw_ingredients.split(',') if i.strip()]
        cleaned_data['ingredients'] = ingredients

        raw_instructions = self.data.get('instructions_text', '')
        instructions = [line.strip()
                        for line in raw_instructions.split('\n')
                        if line.strip()]
        cleaned_data['instructions'] = instructions
        return cleaned_data

    def save(self, commit=True, created_by=None):
        instance = super().save(commit=False)
        instance.ingredients = self.cleaned_data.get('ingredients', [])
        instance.instructions = self.cleaned_data.get('instructions', [])
        if created_by:
            instance.created_by = created_by
        if commit:
            instance.save()
        return instance
