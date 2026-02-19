from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"})
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"})
    )
    phone_number = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "09XXXXXXXXX"})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"})
    )
    telegram_id = forms.CharField(
        label="Telegram ID",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "@yourusername"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"})
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 
            'email', 'telegram_id', 'password1', 'password2'
        ]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Phone or Email",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    

from .validator import mobile_validator

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        return mobile_validator(phone)
