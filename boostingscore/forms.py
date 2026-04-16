from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "bs-auth-input",
                "autocomplete": "email",
                "placeholder": "your@email.com",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "bs-auth-input",
                "autocomplete": "current-password",
                "placeholder": "••••••••••",
            }
        ),
    )


class SignUpForm(forms.Form):
    full_name = forms.CharField(
        label="Full name",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "input", "autocomplete": "name", "placeholder": "Alex Johnson"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "input", "autocomplete": "email", "placeholder": "you@example.com"}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "input", "autocomplete": "new-password", "placeholder": "••••••••"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "input", "autocomplete": "new-password", "placeholder": "••••••••"}
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(username__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_password1(self):
        password = self.cleaned_data["password1"]
        validate_password(password)
        return password

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "The two password fields did not match.")
        return cleaned

    def save(self):
        email = self.cleaned_data["email"]
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=self.cleaned_data["full_name"].strip(),
            password=self.cleaned_data["password1"],
        )
        return user
