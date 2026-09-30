from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your email',
            'style': 'border-radius: 10px; padding: 12px;'
        })
    )
    first_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'First Name',
            'style': 'border-radius: 10px; padding: 12px;'
        })
    )
    last_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Last Name',
            'style': 'border-radius: 10px; padding: 12px;'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username',
            'style': 'border-radius: 10px; padding: 12px;'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Password (min 8 characters)',
            'style': 'border-radius: 10px; padding: 12px;'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirm Password',
            'style': 'border-radius: 10px; padding: 12px;'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username or Email',
            'style': 'border-radius: 10px; padding: 12px;'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Password',
            'style': 'border-radius: 10px; padding: 12px;'
        })
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone', 
            'address', 'city', 'state', 'country', 'zip_code', 'profile_picture'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'border-radius: 10px; padding: 12px;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'border-radius: 10px; padding: 12px;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'border-radius: 10px; padding: 12px;'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'style': 'border-radius: 10px; padding: 12px;', 'placeholder': '+92 300 1234567'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'border-radius: 10px; padding: 12px;', 'placeholder': 'Street address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'style': 'border-radius: 10px; padding: 12px;', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'style': 'border-radius: 10px; padding: 12px;', 'placeholder': 'State/Province'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'style': 'border-radius: 10px; padding: 12px;', 'placeholder': 'Country'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'style': 'border-radius: 10px; padding: 12px;', 'placeholder': 'ZIP/Postal Code'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'style': 'border-radius: 10px; padding: 12px;'}),
        }