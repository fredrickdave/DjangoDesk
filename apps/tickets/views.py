from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TicketAttachmentForm, TicketCommentForm, TicketForm
from .models import Reference, Ticket, TicketAttachment, TicketPriority, TicketStatus


@login_required
def all_user_tickets(request):
    all_tickets = request.user.created_tickets.all()
    context = {"tickets": all_tickets, "page": "all-tickets"}
    return render(request=request, template_name="tickets/all-user-tickets.html", context=context)


@login_required
def ticket_details(request, ticket_number):
    selected_ticket = get_object_or_404(Ticket, ticket_number=ticket_number)
    ticket_comments = selected_ticket.comments.all().order_by("-created_at")
    comment_form = TicketCommentForm()
    attachment_form = TicketAttachmentForm(file_count=selected_ticket.attachments.all())

    if request.method == "POST":
        if "add-comment" in request.POST:
            comment_form = TicketCommentForm(data=request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.created_by = request.user
                comment.ticket = selected_ticket
                comment.save()
                messages.success(request=request, message="Your comment was posted successfully.")
                return redirect(to="ticket-details", ticket_number=ticket_number)
        elif "add-attachment" in request.POST:
            attachment_form = TicketAttachmentForm(
                data=request.POST, files=request.FILES, file_count=selected_ticket.attachments.all()
            )
            if attachment_form.is_valid():
                files = attachment_form.cleaned_data["attachment"]
                create_attachment(files=files, ticket=selected_ticket)
                messages.success(request=request, message="Attachment has been added successfully.")
                return redirect(to="ticket-details", ticket_number=ticket_number)
            else:
                # https://docs.djangoproject.com/en/5.0/ref/forms/api/#django.forms.ErrorList.as_text
                error = attachment_form.errors["attachment"].as_text().replace("*", "")
                messages.error(request=request, message=error)

    context = {
        "selected_ticket": selected_ticket,
        "comment_form": comment_form,
        "attachment_form": attachment_form,
        "ticket_comments": ticket_comments,
    }
    return render(request=request, template_name="tickets/ticket-detail.html", context=context)


def create_attachment(files, ticket):
    """This function accepts a list of Files object

    Args:
        request (_type_): _description_
        files (list): _description_
        ticket (_type_): _description_
    """

    for file in files:
        TicketAttachment.objects.create(attachment=file, ticket=ticket)


@login_required
def create_ticket(request):
    if request.method == "POST":
        ticket_form = TicketForm(data=request.POST, files=request.FILES)
        attachment_form = TicketAttachmentForm(data=request.POST, files=request.FILES)
        if ticket_form.is_valid() and attachment_form.is_valid():
            default_priority = TicketPriority.objects.get(priority=2)
            default_status = TicketStatus.objects.get(status=1)
            ticket = ticket_form.save(commit=False)
            ticket.created_by = request.user
            ticket.ticket_number = Reference.generate(prefix="INC")
            ticket.status = default_status
            ticket.priority_id = default_priority
            ticket.save()

            files = attachment_form.cleaned_data["attachment"]
            create_attachment(files=files, ticket=ticket)
            messages.success(
                request=request,
                message=(
                    f"Your ticket {ticket.ticket_number} has been created. Our support team will get back to you as"
                    " soon as possible."
                ),
            )
            return redirect(to="ticket-details", ticket_number=ticket.ticket_number)
    else:
        ticket_form = TicketForm()
        attachment_form = TicketAttachmentForm()

    context = {"ticket_form": ticket_form, "attachment_form": attachment_form}
    return render(request=request, template_name="tickets/create-ticket.html", context=context)


@login_required
def delete_attachment(request, ticket_number, pk):
    attachment = get_object_or_404(TicketAttachment, id=pk)

    if request.user == attachment.ticket.created_by:
        attachment.delete()
        messages.success(request=request, message="Attachment has been deleted successfully.")
    else:
        messages.error(request=request, message="You are not authorized to perform this action.")
    return redirect(to="ticket-details", ticket_number=ticket_number)
