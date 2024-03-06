from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, render

from ..tickets.models import Ticket


@login_required
def dashboard(request):
    if request.user.role == 3:
        open_count = Ticket.objects.filter(status=1, created_by=request.user).count()
        assigned_count = Ticket.objects.filter(status=2, created_by=request.user).count()
        in_progress_count = Ticket.objects.filter(status=3, created_by=request.user).count()
        on_hold_count = Ticket.objects.filter(status=4, created_by=request.user).count()
        resolved_count = Ticket.objects.filter(status=5, created_by=request.user).count()
        closed_count = Ticket.objects.filter(status=6, created_by=request.user).count()
    elif request.user.role == 1 or request.user.role == 2:
        open_count = Ticket.objects.filter(status=1).count()
        assigned_count = Ticket.objects.filter(status=2, assigned_agent=request.user).count()
        in_progress_count = Ticket.objects.filter(status=3, assigned_agent=request.user).count()
        on_hold_count = Ticket.objects.filter(status=4, assigned_agent=request.user).count()
        resolved_count = Ticket.objects.filter(status=5, assigned_agent=request.user).count()
        closed_count = Ticket.objects.filter(status=6, assigned_agent=request.user).count()

    context = {
        "open_count": open_count,
        "assigned_count": assigned_count,
        "in_progress_count": in_progress_count,
        "on_hold_count": on_hold_count,
        "resolved_count": resolved_count,
        "closed_count": closed_count,
        "page": "dashboard",
    }
    return render(request=request, template_name="core/dashboard.html", context=context)
