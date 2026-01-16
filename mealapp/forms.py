from datetime import date, datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from .models import MealPlan, UserProfile, Recipe


class CustomRegistrationForm(UserCreationForm):
    """
    Extended user registration form with email and validation
    """
    username = forms.CharField(
        max_length=150,
        min_length=3,
        required=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        help_text='Enter a strong password.'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter password'
        }),
        help_text='Enter the same password again for verification.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            })
        }
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower().strip()
        # Check if email already exists
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Check minimum length
        if len(username) < 3:
            raise forms.ValidationError(
                "Username must be at least 3 characters long."
            )
        # Check if username exists (case-insensitive)
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "This username is already taken."
            )
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if not password1:
            return password1

        # Minimum length
        if len(password1) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters long."
            )

        # Uppercase letter
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        # Number
        if not re.search(r'\d', password1):
            raise forms.ValidationError(
                "Password must contain at least one number."
            )

        # Special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError(
                "Password must contain at least one special character."
            )

        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "The two password fields didn't match."
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileSetupForm(forms.ModelForm):
    """Form for setting up user profile"""

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'age',
                  'weight_kg', 'height_cm', 'gender', 'user_image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Enter your age'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Enter your weight (kg)'}),
            'height_cm': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Enter your height (cm)'}),

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
