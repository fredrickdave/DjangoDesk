from django import forms
from django.forms import ModelForm

from .models import Ticket


class TicketForm(ModelForm):
    # https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/#overriding-the-default-fields
    class Meta:
        model = Ticket
        fields = ["summary", "issue_type", "description"]

        widgets = {
            "summary": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "issue_type": forms.Select(attrs={"class": "form-control"}),
        }

        labels = {
            "summary": "Ticket Summary",
            "description": "Description",
            "issue_type": "Issue Type",
        }

        error_class = "invalid-feedback"
