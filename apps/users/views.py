from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import EditProfileForm, LoginForm, RegisterForm
from .models import User


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
                messages.success(request, "You have sucessfully logged in.")
                next_url = request.POST.get("next")

                # Check if "?next=" param is safe (not off-site).
                if next_url and url_has_allowed_host_and_scheme(next_url, None):
                    next_url = iri_to_uri(next_url)
                    return redirect(to=next_url)
                return redirect("dashboard")
            else:
                messages.error(request=request, message="Incorrect Email or Password. Please try again.")
                return redirect("login")
    else:
        login_form = LoginForm()

    context = {"login_form": login_form}
    return render(request=request, template_name="users/login.html", context=context)


def sign_out(request):
    logout(request=request)
    messages.success(request, "You have sucessfully logged out.")
    return redirect("login")


def register(request):
    # Redirect to dashboard if user is already logged-in
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, "You are now registered. Log in using your registered Email and Password.")
            return redirect("login")
    else:
        register_form = RegisterForm()

    context = {"register_form": register_form}
    return render(request=request, template_name="users/register.html", context=context)


def profile(request, email):
    edit_profile_form = EditProfileForm(instance=request.user)
    user = User.objects.get(email=email)
    context = {"user": user, "edit_profile_form": edit_profile_form}
    return render(request=request, template_name="users/profile.html", context=context)
