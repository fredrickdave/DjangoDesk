import django_tables2 as tables
from django.urls import reverse

from .models import Ticket


class TicketTable(tables.Table):
    ticket_number = tables.Column(linkify=True)

    class Meta:
        model = Ticket
        template_name = "tickets/table/bootstrap-htmx.html"
        fields = (
            "ticket_number",
            "summary",
            "issue_type",
            "status",
            "created_at",
            "created_by",
        )
