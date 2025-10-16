from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control bg-white text-dark", "placeholder": "Password"}),
        label="Password"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control bg-white text-dark", "placeholder": "Confirm Password"}),
        label="Confirm Password"
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control bg-white text-dark", "placeholder": "Username"}),
        label="Username"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control bg-white text-dark", "placeholder": "Email"}),
        label="Email"
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")
        return cleaned_data


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control bg-white text-dark"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control bg-white text-dark"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control bg-white text-dark", "rows": 6})
    )



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control bg-white text-dark", "placeholder": "Email address"})
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control bg-white text-dark", "placeholder": "Username"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control bg-white text-dark", "placeholder": "Password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control bg-white text-dark", "placeholder": "Confirm Password"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
