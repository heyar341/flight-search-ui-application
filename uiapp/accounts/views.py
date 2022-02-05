import django.http.response
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from os import environ
import requests
import logging

from .forms import RegisterForm, PreRegisterForm
from .publisher import publish_message

logger = logging.getLogger(__name__)


class PreRegistrationView(FormView):
    template_name = "accounts/pre_register.html"
    form_class = PreRegisterForm
    success_url = "pre_register_success"

    def form_valid(self,
                   form: RegisterForm) -> django.http.response.HttpResponse:
        email_address = form.cleaned_data["email"]
        queue_name = environ.get("EMAIL_REGISTER_QUEUE_NAME")
        publish_message(email=email_address, queue_name=queue_name)
        return HttpResponseRedirect(self.get_success_url())


def pre_register_success(
        request: django.http.HttpRequest) -> django.http.response.HttpResponse:
    return render(request, "accounts/pre_register_success.html", None)


class RegistrationView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = "register_success"

    def form_valid(self,
                   form: RegisterForm) -> django.http.response.HttpResponse:
        user_data = form.cleaned_data
        user_data["password"] = user_data.pop("password1")
        user_data.pop("password2")
        user_service_endpoint = environ.get("USER_SERVICE_ENDPOINT")

        try:
            response = requests.post(url=user_service_endpoint + "/register",
                                     json=user_data, timeout=3.0)
        except requests.ConnectionError as e:
            logger.error(
                f"Error while sending user json data to user service.\n{e}")
            return super().render_to_response(
                super().get_context_data(form=form))
        except requests.Timeout as e:
            logger.error(
                f"Timeout while sending user json data to user service.\n{e}")
            return super().render_to_response(
                super().get_context_data(form=form))

        if response.status_code == 200:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super().render_to_response(
                super().get_context_data(form=form))


def register_success(
        request: django.http.HttpRequest) -> django.http.response.HttpResponse:
    return render(request, "accounts/register_success.html", None)
