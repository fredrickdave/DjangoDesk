from django.shortcuts import HttpResponse, render

from .models import Ticket


# Create your views here.
def index(request):
    return HttpResponse("Tickets Module")


def ticket_details(request, pk):
    selected_ticket = Ticket.objects.get(id=pk)
    context = {"selected_ticket": selected_ticket, "num": range(50)}
    return render(request=request, template_name="tickets/ticket-detail.html", context=context)
