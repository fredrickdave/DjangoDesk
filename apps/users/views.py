from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.safestring import mark_safe

from .forms import ChangeEmailForm, ChangePasswordForm, EditProfileForm, LoginForm, RegisterForm, TimeZoneForm


def sign_in(request):
    # Redirect to dashboard if user is already logged-in
    if request.user.is_authenticated:
        return redirect("dashboard")

    login_form = LoginForm()
    context = {"login_form": login_form}

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # https://docs.djangoproject.com/en/4.2/ref/forms/api/#accessing-clean-data
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request=request, user=user)
                messages.success(request=request, message="You have sucessfully logged in.")
                next_url = request.POST.get("next")

                # Check if "?next=" param is safe (not off-site).
                if next_url and url_has_allowed_host_and_scheme(next_url, None):
                    next_url = iri_to_uri(next_url)
                    return redirect(to=next_url)
                return redirect("dashboard")
            else:
                messages.error(request=request, message="Incorrect Email or Password. Please try again.")
                return render(request=request, template_name="users/login.html", context=context)
    else:
        messages.warning(
            request=request,
            message=mark_safe(
                """For demo purposes, use the following accounts:<br/><br/>

                Customer Account<br/>
                Email: <b>democustomer@demo.com</b><br/>
                Password: <b>demo1234</b><br/><br/>

                Support Agent Account<br/>
                Email: <b>demoagent@demo.com</b><br/>
                Password: <b>demo1234</b>"""
            ),
        )

    return render(request=request, template_name="users/login.html", context=context)


def sign_out(request):
    logout(request=request)
    messages.success(request=request, message="You have sucessfully logged out.")
    return redirect("login")


def register(request):
    # Redirect to dashboard if user is already logged-in
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(
                request=request, message="You are now registered. Log in using your registered Email and Password."
            )
            return redirect("login")
    else:
        register_form = RegisterForm()

    context = {"register_form": register_form}
    return render(request=request, template_name="users/register.html", context=context)


@login_required
def profile(request):
    edit_profile_form = EditProfileForm(instance=request.user)
    change_password_form = ChangePasswordForm(user=request.user)
    change_email_form = ChangeEmailForm(instance=request.user, request=request)
    change_timezone_form = TimeZoneForm(instance=request.user)

    if request.method == "POST":
        if "update-profile" in request.POST:
            edit_profile_form = EditProfileForm(data=request.POST, files=request.FILES, instance=request.user)
            if edit_profile_form.is_valid():
                edit_profile_form.save()
                messages.success(request=request, message="You have successfully updated your profile details.")
        elif "update-password" in request.POST:
            change_password_form = ChangePasswordForm(user=request.user, data=request.POST)
            if change_password_form.is_valid():
                change_password_form.save()
                # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.update_session_auth_hash
                update_session_auth_hash(request=request, user=change_password_form.user)
                messages.success(request=request, message="You have successfully changed your password.")
            else:
                messages.error(request=request, message="Password change failed. Please try again.")
        elif "update-email" in request.POST:
            change_email_form = ChangeEmailForm(instance=request.user, data=request.POST, request=request)
            if change_email_form.is_valid():
                change_email_form.save()
                messages.success(request=request, message="You have successfully changed your email.")
            else:
                messages.error(request=request, message="Email change failed. Please try again.")
        elif "update-settings" in request.POST:
            change_timezone_form = TimeZoneForm(data=request.POST, files=request.FILES, instance=request.user)
            if change_timezone_form.is_valid():
                change_timezone_form.save()
                messages.success(request=request, message="You have successfully updated your Time Zone.")

    context = {
        "edit_profile_form": edit_profile_form,
        "change_email_form": change_email_form,
        "change_password_form": change_password_form,
        "change_timezone_form": change_timezone_form,
        "page": "profile",
    }
    return render(request=request, template_name="users/profile.html", context=context)
