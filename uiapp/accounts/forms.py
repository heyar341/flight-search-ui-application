from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField, Form, EmailInput


class PreRegisterForm(Form):
    email = EmailField(label="Email", widget=EmailInput)


class RegisterForm(UserCreationForm):
    email = EmailField(label="Email", widget=EmailInput)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=None):
        pass
