import os

import magic
from django.core.exceptions import ValidationError
from django.db import models
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


class TicketType(BaseModel):
    class Type(models.IntegerChoices):
        SERVICE_REQUEST = 1, "Service Request"
        INCIDENT = 2, "Incident"
        PROBLEM = 3, "Problem"
        CHANGE_REQUEST = 4, "Change Request"

    type = models.IntegerField(choices=Type.choices)

    def __str__(self) -> str:
        # https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.get_FOO_display
        return self.get_type_display()


class TicketStatus(BaseModel):
    class Status(models.IntegerChoices):
        OPEN = 1, "Open"
        ASSIGNED = 2, "Assigned"
        IN_PROGRESS = 3, "In Progress"
        ON_HOLD = 4, "On Hold"
        RESOLVED = 5, "Resolved"
        CLOSED = 6, "Closed"

    status = models.IntegerField(choices=Status.choices)

    class Meta:
        verbose_name_plural = "Ticket Status"

    def __str__(self) -> str:
        # https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.get_FOO_display
        return self.get_status_display()


class TicketPriority(BaseModel):
    class Priority(models.IntegerChoices):
        HIGH = "1", "High"
        MEDIUM = "2", "Medium"
        LOW = "3", "Low"

    priority = models.IntegerField(choices=Priority.choices)

    class Meta:
        verbose_name_plural = "Ticket Priorities"

    def __str__(self) -> str:
        # https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.get_FOO_display
        return self.get_priority_display()


class TicketActivity(BaseModel):
    activity = models.TextField()
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="ticket_activities")

    def __str__(self) -> str:
        return self.activity


class Ticket(BaseModel):
    ticket_number = models.CharField(max_length=25, unique=True, db_index=True)
    summary = models.CharField(max_length=100, null=True)
    description = models.TextField()
    issue_type = models.ForeignKey(TicketType, null=True, on_delete=models.SET_NULL, related_name="tickets")
    assigned_agent = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_tickets"
    )
    status = models.ForeignKey(TicketStatus, null=True, blank=True, on_delete=models.SET_NULL, related_name="tickets")
    priority_id = models.ForeignKey(
        TicketPriority, null=True, blank=True, on_delete=models.SET_NULL, related_name="tickets"
    )
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_tickets"
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.summary


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

    @property
    def attachment_name(self):
        return os.path.basename(self.attachment.name)

    @property
    def url(self):
        return self.attachment.url
