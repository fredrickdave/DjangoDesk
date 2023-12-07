from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm

from .models import User

# Don't use modelform for login page to avoid validation error
# https://stackoverflow.com/questions/23103570/how-to-stop-the-user-is-already-exist-validation-in-django
# class LoginForm(ModelForm):
#     # https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/#overriding-the-default-fields
#     class Meta:
#         model = User
#         fields = ["email", "password"]

#         widgets = {
#             "email": forms.EmailInput(attrs={"class": "form-control"}),
#             "password": forms.PasswordInput(attrs={"class": "form-control"}),
#         }


class LoginForm(forms.Form):
    username = forms.EmailField(label="Email", max_length=100, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))


class RegisterForm(UserCreationForm):
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.forms.UserCreationForm
    # Redefined password fields to add css class. Meta.widgets does not work on these since these are not
    # fields from the User model and are "custom" fields from the UserCreationForm
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        strip=False,
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ["email"]

        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
        }


class ChangePasswordForm(PasswordChangeForm):
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.forms.PasswordChangeForm
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.update_session_auth_hash
    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "current-password", "autofocus": True}
        ),
    )

    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
        strip=False,
    )

    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "new-password"}),
    )


class ChangeEmailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs["request"] is not None:
            self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_email(self):
        data = self.cleaned_data["email"]

        if data == self.request.user.email:
            raise forms.ValidationError("You entered the same email you are already using.")

        return data

    class Meta:
        model = User
        fields = ["email"]

        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class CustomClearableFileInput(forms.ClearableFileInput):
    clear_checkbox_label = "Remove profile image"
    input_text = "Add/Change profile image"
    template_name = "users/includes/clearable_file_input.html"


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "first_name", "last_name", "about", "job", "department", "company", "phone", "linkedin"]

        widgets = {
            "avatar": CustomClearableFileInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "about": forms.Textarea(attrs={"class": "form-control", "style": "height:100px"}),
            "job": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "linkedin": forms.URLInput(attrs={"class": "form-control"}),
        }
