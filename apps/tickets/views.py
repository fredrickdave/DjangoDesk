from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import TicketForm
from .models import Reference, Ticket, TicketPriority, TicketStatus


@login_required
def all_tickets(request):
    all_tickets = Ticket.objects.all()
    context = {"tickets": all_tickets}
    return render(request=request, template_name="tickets/all-tickets.html", context=context)


@login_required
def ticket_details(request, ticket_number):
    selected_ticket = Ticket.objects.get(ticket_number=ticket_number)
    context = {"selected_ticket": selected_ticket, "num": range(50)}
    return render(request=request, template_name="tickets/ticket-detail.html", context=context)


@login_required
def create_ticket(request):
    default_priority = TicketPriority.objects.get(priority=2)
    default_status = TicketStatus.objects.get(status=1)

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.ticket_number = Reference.generate(prefix="INC")
            ticket.status = default_status
            ticket.priority_id = default_priority
            ticket.save()
            return redirect("dashboard")
    else:
        form = TicketForm()

    context = {"ticket_form": form}
    return render(request=request, template_name="tickets/create-ticket.html", context=context)
