from django import forms
from django.forms import ModelForm

from .models import Ticket, TicketComment


class TicketForm(ModelForm):
    # https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/#overriding-the-default-fields
    class Meta:
        model = Ticket
        fields = ["summary", "issue_type", "attachment", "description"]

        widgets = {
            "summary": forms.TextInput(attrs={"class": "form-control"}),
            "issue_type": forms.Select(attrs={"class": "form-control"}),
            "attachment": forms.FileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }

        labels = {
            "summary": "Ticket Summary (Required)",
            "description": "Description (Required)",
            "issue_type": "Issue Type (Required)",
            "attachment": "Issue Type (Optional)",
        }

        error_class = "invalid-feedback"


class TicketCommentForm(ModelForm):
    class Meta:
        model = TicketComment
        fields = ["comment"]

        widgets = {"comment": forms.Textarea(attrs={"class": "form-control ticket-comment"})}
        labels = {"comment": "Add notes:"}
