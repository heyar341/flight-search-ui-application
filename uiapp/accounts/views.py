import django.http.response
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from os import environ
import requests
import logging

from .forms import RegisterForm

USER_SERVICE_ENDPOINT = environ["USER_SERVICE_ENDPOINT"]

logger = logging.getLogger(__name__)


class RegistrationView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = "register_success"

    def form_valid(self,
                   form: RegisterForm) -> django.http.response.HttpResponse:
        user_data = form.cleaned_data
        user_data["password"] = user_data.pop("password1")
        user_data.pop("password2")
        try:
            response = requests.post(url=USER_SERVICE_ENDPOINT + "/register",
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


def register_success(request):
    return render(request, "accounts/register_success.html", None)
