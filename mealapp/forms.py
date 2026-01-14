from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re


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
