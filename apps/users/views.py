from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm


# Create your views here.
def sign_in(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # https://docs.djangoproject.com/en/4.2/ref/forms/api/#accessing-clean-data
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request=request, user=user)
                return redirect(to="dashboard")
    else:
        login_form = LoginForm()

    context = {"login_form": login_form}
    return render(request=request, template_name="users/login.html", context=context)


def sign_out(request):
    logout(request=request)
    return redirect("login")
