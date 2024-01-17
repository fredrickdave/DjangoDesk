import django_filters

from .models import Ticket


class TicketFilter(django_filters.FilterSet):
    ticket_number = django_filters.CharFilter(label="Ticket Number", lookup_expr="icontains")
    summary = django_filters.CharFilter(label="Summary", lookup_expr="icontains")
    created_at = django_filters.DateRangeFilter(label="Date Created")

    class Meta:
        model = Ticket
        fields = {"ticket_number", "summary", "issue_type", "status", "created_at"}

    # https://django-filter.readthedocs.io/en/stable/guide/usage.html#request-based-filtering
    @property
    def qs(self):
        parent = super().qs
        author = getattr(self.request, "user", None)

        return parent.filter(created_by=author)
