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

        # Override qs method to filter tickets based on user's role. Show user's created tickets if customer.
        # Show all tickets if support agent or Admin
        if self.request.user.role == 3:
            return parent.filter(created_by=author)
        elif self.request.user.role == 1 or self.request.user.role == 2:
            return parent
