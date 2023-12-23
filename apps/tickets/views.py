from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TicketCommentForm, TicketForm
from .models import Reference, Ticket, TicketPriority, TicketStatus


@login_required
def all_user_tickets(request):
    all_tickets = request.user.created_tickets.all()
    context = {"tickets": all_tickets, "page": "all-tickets"}
    return render(request=request, template_name="tickets/all-user-tickets.html", context=context)


@login_required
def ticket_details(request, ticket_number):
    comment_form = TicketCommentForm()
    selected_ticket = get_object_or_404(Ticket, ticket_number=ticket_number)
    ticket_comments = selected_ticket.comments.all().order_by("-created_at")

    if request.method == "POST":
        comment_form = TicketCommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.created_by = request.user
            comment.tickets = selected_ticket
            comment.save()
            messages.success(request=request, message="Your comment was posted successfully.")
            return redirect(to="ticket-details", ticket_number=ticket_number)

    context = {"selected_ticket": selected_ticket, "comment_form": comment_form, "ticket_comments": ticket_comments}
    return render(request=request, template_name="tickets/ticket-detail.html", context=context)


@login_required
def create_ticket(request):
    default_priority = TicketPriority.objects.get(priority=2)
    default_status = TicketStatus.objects.get(status=1)

    if request.method == "POST":
        form = TicketForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.ticket_number = Reference.generate(prefix="INC")
            ticket.status = default_status
            ticket.priority_id = default_priority
            ticket.save()
            return redirect(to="dashboard")
    else:
        form = TicketForm()

    context = {"ticket_form": form}
    return render(request=request, template_name="tickets/create-ticket.html", context=context)
