from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, redirect, render
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm, RegisterForm


def sign_in(request):
    # Redirect to dashboard if user is already logged-in
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # https://docs.djangoproject.com/en/4.2/ref/forms/api/#accessing-clean-data
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request=request, user=user)
                next_url = request.POST.get("next")

                # Check if "?next=" param is safe (not off-site).
                if next_url and url_has_allowed_host_and_scheme(next_url, None):
                    next_url = iri_to_uri(next_url)
                    return redirect(to=next_url)
                return redirect("dashboard")
            else:
                return redirect("login")
    else:
        login_form = LoginForm()

    context = {"login_form": login_form}
    return render(request=request, template_name="users/login.html", context=context)


def sign_out(request):
    logout(request=request)
    return redirect("login")


def register(request):
    # Redirect to dashboard if user is already logged-in
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            print("Registered")
            return redirect("dashboard")
    else:
        register_form = RegisterForm()

    context = {"register_form": register_form}
    return render(request=request, template_name="users/register.html", context=context)
