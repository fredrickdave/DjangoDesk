import django_tables2 as tables
from django.urls import reverse

from .models import Ticket


class TicketTable(tables.Table):
    ticket_number = tables.Column(linkify=True)

    class Meta:
        model = Ticket
        template_name = "django_tables2/bootstrap5-responsive.html"
        fields = (
            "ticket_number",
            "summary",
            "status",
            "created_by",
            "created_at",
        )
