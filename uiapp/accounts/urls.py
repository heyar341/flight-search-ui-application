from django.urls import path
from .views import RegistrationView, register_success, PreRegistrationView, \
    pre_register_success

urlpatterns = [
    path("pre_register", PreRegistrationView.as_view(), name="pre_register"),
    path("pre_register_success", pre_register_success,
         name="pre_register_success"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("register_success", register_success, name="register_success"),
]
