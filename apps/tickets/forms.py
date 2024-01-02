from django import forms
from django.forms import ModelForm

from .models import Ticket, TicketAttachment, TicketComment, validate_file_size


class TicketForm(ModelForm):
    # https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/#overriding-the-default-fields
    class Meta:
        model = Ticket
        fields = ["summary", "issue_type", "description"]

        widgets = {
            "summary": forms.TextInput(attrs={"class": "form-control"}),
            "issue_type": forms.Select(attrs={"class": "form-control"}),
            # "attachment": forms.FileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }

        labels = {
            "summary": "Ticket Summary (Required)",
            "description": "Description (Required)",
            "issue_type": "Issue Type (Required)",
            # "attachment": "Issue Type (Optional)",
        }

        error_class = "invalid-feedback"


class TicketCommentForm(ModelForm):
    class Meta:
        model = TicketComment
        fields = ["comment"]

        widgets = {"comment": forms.Textarea(attrs={"class": "form-control ticket-comment"})}
        labels = {"comment": "Add notes:"}


# https://docs.djangoproject.com/en/5.0/topics/http/file-uploads/#uploading-multiple-files
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={"class": "form-control"}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class TicketAttachmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.max_files = 10
        if kwargs["file_count"] is not None:
            self.file_count = kwargs.pop("file_count")
        super().__init__(*args, **kwargs)

    def clean_attachment(self):
        data = self.cleaned_data["attachment"]

        if (len(data) + len(self.file_count.all())) > self.max_files:
            raise forms.ValidationError(f"You can upload up to {self.max_files} files only.")

        return data

    class Meta:
        model = TicketAttachment
        fields = ["attachment"]

    attachment = MultipleFileField(
        label="Attachment (Add up to 10 files. Max file size: 10 MB):", validators=[validate_file_size]
    )
