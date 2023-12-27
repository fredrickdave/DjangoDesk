from django.urls import path

from . import views

urlpatterns = [
    path("", views.all_user_tickets, name="all-tickets"),
    path("details/<ticket_number>/", views.ticket_details, name="ticket-details"),
    path("details/<ticket_number>/attachment/<int:pk>/delete/", views.delete_attachment, name="delete-attachment"),
    path("create/", views.create_ticket, name="create-ticket"),
]
