import os

import magic
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from ..users.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # https://docs.djangoproject.com/en/4.2/topics/db/models/#abstract-base-classes
    class Meta:
        abstract = True


class Reference(models.Model):
    """Generate unique reference numbers for other models.

    The only purpose of this model is to generate unique reference numbers.
    """

    # Django models need at least 1 field
    created_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate(cls, prefix: str) -> str:
        """Generate a unique reference number prefixed with the provided prefix.

        For example, you could generate an invoice number as follows:

        Reference.generate(prefix="INV") # INV-0000001 etc.
        """

        instance = cls.objects.create()
        suffix = f"{instance.pk}".zfill(7)
        return f"{prefix}-{suffix}"


class TicketActivity(BaseModel):
    activity = models.TextField()
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="ticket_activities")

    def __str__(self) -> str:
        return self.activity


class Ticket(BaseModel):
    class Status(models.IntegerChoices):
        OPEN = 1, "Open"
        ASSIGNED = 2, "Assigned"
        IN_PROGRESS = 3, "In Progress"
        ON_HOLD = 4, "On Hold"
        RESOLVED = 5, "Resolved"
        CLOSED = 6, "Closed"

    class Priority(models.IntegerChoices):
        HIGH = "1", "High"
        MEDIUM = "2", "Medium"
        LOW = "3", "Low"

    class Type(models.IntegerChoices):
        SERVICE_REQUEST = 1, "Service Request"
        INCIDENT = 2, "Incident"
        PROBLEM = 3, "Problem"
        CHANGE_REQUEST = 4, "Change Request"

    ticket_number = models.CharField(max_length=25, unique=True, db_index=True)
    summary = models.CharField(max_length=100)
    description = models.TextField()
    issue_type = models.IntegerField(choices=Type.choices)
    assigned_agent = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_tickets"
    )
    status = models.IntegerField(choices=Status.choices, default=Status.OPEN)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.LOW)

    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_tickets"
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.ticket_number} - {self.summary}"

    def get_absolute_url(self):
        """This is used by the table to generate a link to the ticket detail page."""
        return reverse("ticket-details", kwargs={"ticket_number": self.ticket_number})

    def assign(self, user):
        self.assigned_agent = user
        self.save()


class TicketComment(BaseModel):
    comment = models.TextField()
    ticket = models.ForeignKey(Ticket, null=True, on_delete=models.SET_NULL, related_name="comments")
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="comments")

    def __str__(self) -> str:
        return self.comment


def attachment_directory_path(instance, filename):
    return f"ticketfiles/{instance.ticket.id}/{filename}"


def validate_file_size(value):
    limit = 10 * 1024 * 1024  # 10 MB

    if isinstance(value, (list, tuple)):
        for file in value:
            if file.size > limit:
                raise ValidationError("File too large. Size should not exceed 10 MB.")
    else:
        if value.size > limit:
            raise ValidationError("File too large. Size should not exceed 10 MB.")


def validate_file_type(value):
    blacklisted_mime_types = ["application/x-msdownload", "application/x-dosexec", "application/CDFV2"]
    blacklisted_file_extensions = [".exe", ".msi", ".cmd", ".bat"]

    if isinstance(value, (list, tuple)):
        for file in value:
            file_mime_type = magic.from_buffer(file.read(2048), mime=True)
            ext = os.path.splitext(file.name)[1]
            print("MIME", file_mime_type)
            print("EXT", ext)
            if file_mime_type in blacklisted_mime_types or ext in blacklisted_file_extensions:
                raise ValidationError("Unsupported file type.")
    else:
        file_mime_type = magic.from_buffer(value.read(2048), mime=True)
        if file_mime_type in blacklisted_mime_types:
            raise ValidationError("Unsupported file type.")


class TicketAttachment(BaseModel):
    attachment = models.FileField(
        upload_to=attachment_directory_path, validators=[validate_file_size, validate_file_type], null=True, blank=True
    )
    ticket = models.ForeignKey(Ticket, null=True, on_delete=models.CASCADE, related_name="attachments")

    def __str__(self) -> str:
        return self.attachment.name

    @property
    def attachment_name(self):
        return os.path.basename(self.attachment.name)

    @property
    def url(self):
        return self.attachment.url
