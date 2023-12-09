from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import TicketForm
from .models import Reference, Ticket, TicketPriority, TicketStatus


@login_required
def all_user_tickets(request):
    all_tickets = request.user.created_tickets.all()
    context = {"tickets": all_tickets, "page": "all-tickets"}
    return render(request=request, template_name="tickets/all-user-tickets.html", context=context)


@login_required
def ticket_details(request, ticket_number):
    selected_ticket = Ticket.objects.get(ticket_number=ticket_number)
    context = {"selected_ticket": selected_ticket, "num": range(50)}
    print(request.user.created_tickets.all())
    return render(request=request, template_name="tickets/ticket-detail.html", context=context)


@login_required
def create_ticket(request):
    default_priority = TicketPriority.objects.get(priority=2)
    default_status = TicketStatus.objects.get(status=1)

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.ticket_number = Reference.generate(prefix="INC")
            ticket.status = default_status
            ticket.priority_id = default_priority
            ticket.save()
            return redirect("dashboard")
    else:
        form = TicketForm()

    context = {"ticket_form": form}
    return render(request=request, template_name="tickets/create-ticket.html", context=context)
