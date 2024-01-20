from django.urls import path

from . import views

urlpatterns = [
    path("", views.TableView.as_view(), name="all-tickets"),
    path("create/", views.create_ticket, name="create-ticket"),
    path("<ticket_number>/", views.ticket_details, name="ticket-details"),
    path("<ticket_number>/assign", views.assign_ticket, name="assign-ticket"),
    path("<ticket_number>/delete/attachment/<int:pk>/", views.delete_attachment, name="delete-attachment"),
]
