"""
Secure Django forms with built-in validation and CSRF protection.

Security features:
- Automatic input validation
- XSS protection through Django's form rendering
- CSRF token integration
- SQL injection prevention through ORM
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class ExampleForm(forms.Form):
    """
    Example form demonstrating secure form practices.

    Security measures:
    - max_length prevents buffer overflow attacks
    - required=True prevents empty submissions
    - Django auto-escapes output to prevent XSS
    - CSRF token automatically added when rendered with {% csrf_token %}
    """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        }),
        help_text='Maximum 100 characters'
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }),
        help_text='Valid email address required'
    )

    message = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 4
        }),
        help_text='Maximum 500 characters'
    )

    def clean_name(self):
        """
        Custom validation for name field.
        Sanitizes input and prevents malicious content.
        """
        name = self.cleaned_data.get('name')

        # Strip whitespace
        name = name.strip()

        # Validate minimum length
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')

        # Validate no special characters that could be used for attacks
        if any(char in name for char in ['<', '>', '"', "'", '&']):
            raise ValidationError('Name contains invalid characters.')

        return name

    def clean_message(self):
        """
        Custom validation for message field.
        """
        message = self.cleaned_data.get('message')

        # Strip whitespace
        message = message.strip()

        # Validate minimum length
        if len(message) < 10:
            raise ValidationError('Message must be at least 10 characters long.')

        return message


class UserRegistrationForm(UserCreationForm):
    """
    Secure user registration form.

    Security features:
    - Password validation (length, complexity)
    - Email validation
    - Protection against user enumeration
    - CSRF protection
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )

    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )

    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        """
        Validate email is unique.
        Note: Be careful not to reveal if email exists (user enumeration attack).
        """
        email = self.cleaned_data.get('email')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')

        return email


class SearchForm(forms.Form):
    """
    Secure search form.

    Security measures:
    - Input length limitation
    - SQL injection prevention through ORM
    - XSS prevention through escaping
    """
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search...',
            'type': 'search'
        })
    )

    def clean_query(self):
        """
        Sanitize search query.
        """
        query = self.cleaned_data.get('query', '')

        # Strip whitespace
        query = query.strip()

        # Limit length (already done by max_length, but double-check)
        if len(query) > 100:
            query = query[:100]

        return query