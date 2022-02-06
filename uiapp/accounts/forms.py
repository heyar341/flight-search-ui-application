from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import (EmailField, Form, EmailInput, HiddenInput, CharField,
                          PasswordInput)


class PreRegisterForm(Form):
    email = EmailField(label="Email", widget=EmailInput())


class RegisterForm(UserCreationForm):
    email = EmailField(widget=HiddenInput())
    email_token = CharField(widget=HiddenInput())

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "email_token")

    def save(self, commit=None):
        pass


class LoginForm(Form):
    email = EmailField(label="Email", widget=EmailInput())
    password = CharField(label="Password", widget=PasswordInput())
