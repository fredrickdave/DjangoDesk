from django.shortcuts import HttpResponse, redirect, render

from .forms import TicketForm
from .models import Ticket, TicketPriority, TicketStatus


# Create your views here.
def index(request):
    return HttpResponse("Tickets Module")


def ticket_details(request, pk):
    selected_ticket = Ticket.objects.get(id=pk)
    context = {"selected_ticket": selected_ticket, "num": range(50)}
    return render(request=request, template_name="tickets/ticket-detail.html", context=context)


def create_ticket(request):
    default_priority = TicketPriority.objects.get(priority=2)
    default_status = TicketStatus.objects.get(status=1)

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.status = default_status
            ticket.priority_id = default_priority
            ticket.save()
            return redirect("dashboard")
    else:
        form = TicketForm()

    context = {"ticket_form": form}
    return render(request=request, template_name="tickets/create-ticket.html", context=context)
