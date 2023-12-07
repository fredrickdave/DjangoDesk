from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.sign_in, name="login"),
    path("logout/", views.sign_out, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("change-password/", views.change_password, name="change-password"),
    path("change-email/", views.change_email, name="change-email"),
]
