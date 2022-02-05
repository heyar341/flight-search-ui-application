from django.urls import path
from .views import RegistrationView, register_success

urlpatterns = [
    path("register", RegistrationView.as_view(), name="register"),
    path("register_success", register_success, name="register_success"),
]
