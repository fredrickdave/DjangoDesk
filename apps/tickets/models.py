import os

import magic
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from simple_history.models import HistoricalRecords

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
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.ticket_number} - {self.summary}"

    def get_absolute_url(self):
        """This is used by django_tables2 to generate a link to the ticket detail page."""
        return reverse("ticket-details", kwargs={"ticket_number": self.ticket_number})

    def assign_agent(self, user: User):
        """This method accepts a User object, verifies it's role is either an admin or support agent and not the ticket
        author, then assigns it to the ticket's assigned agent field.

        Args:
            user (User): instance of user object that will be assigned to the ticket
        """
        if user.role == 1 or user.role == 2 and user != self.created_by:
            self.assigned_agent = user

    def set_status_open(self):
        "Sets the ticket status to Open. If an agent was already assigned to ticket, status will be Assigned instead."
        if self.assigned_agent:
            self.status = 2
            self._change_reason = f"Ticket has been reopened and reassigned to {self.assigned_agent}."
        else:
            self.status = 1
            self._change_reason = "Ticket has been reopened."

    def set_status_assigned(self):
        "Set the ticket status to Assigned."
        self.status = 2
        self._change_reason = f"Ticket has been assigned to {self.assigned_agent}."

    def set_status_in_progress(self):
        "Set the ticket status to In Progress."
        if self.status == 4:
            self._change_reason = "Work on the ticket has resumed."
        elif self.status == 2:
            self._change_reason = "Work on the ticket has started."
        else:
            self._change_reason = "Ticket is now In Progress."
        self.status = 3

    def set_status_on_hold(self):
        "Set the ticket status to On Hold."
        self.status = 4
        self._change_reason = "Ticket has been put on hold status."

    def set_status_resolved(self):
        "Set the ticket status to Resolved."
        self.status = 5
        self._change_reason = "Ticket has been resolved."

    def set_status_close(self):
        "Set the ticket status to Closed."
        self.status = 6
        self._change_reason = "Ticket has been closed."


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

    def delete(self, *args, **kwargs):
        super(TicketAttachment, self).delete(*args, **kwargs)
        self.ticket._change_reason = "File attachment was deleted from the ticket."
        self.ticket.save()

    def save(self, *args, **kwargs):
        super(TicketAttachment, self).save(*args, **kwargs)
        self.ticket._change_reason = "File attachment was added to the ticket."
        self.ticket.save()
