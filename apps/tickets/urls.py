from django.urls import path

from . import views

urlpatterns = [
    path("", views.all_tickets, name="all-tickets"),
    path("details/<ticket_number>/", views.ticket_details, name="ticket-details"),
    path("create/", views.create_ticket, name="create-ticket"),
]
