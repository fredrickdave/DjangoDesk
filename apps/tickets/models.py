from django.db import models
from django.utils import timezone

from ..users.models import User


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # https://docs.djangoproject.com/en/4.2/topics/db/models/#abstract-base-classes
    class Meta:
        abstract = True


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


class TicketComment(BaseModel):
    comment = models.TextField()
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="author")

    def __str__(self) -> str:
        return self.comment


class Ticket(BaseModel):
    # ticket_uuid =
    ticket_summary = models.CharField(max_length=100, null=True)
    description = models.TextField()
    issue_type = models.ForeignKey(TicketType, null=True, blank=True, on_delete=models.SET_NULL, related_name="tickets")
    assigned_agent = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="agent")
    status = models.ForeignKey(TicketStatus, null=True, blank=True, on_delete=models.SET_NULL, related_name="tickets")
    priority_id = models.ForeignKey(
        TicketPriority, null=True, blank=True, on_delete=models.SET_NULL, related_name="tickets"
    )
    comments = models.ForeignKey(
        TicketComment, null=True, blank=True, on_delete=models.SET_NULL, related_name="tickets"
    )
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="user")
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.ticket_summary
