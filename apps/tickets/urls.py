from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("details/<int:pk>/", views.ticket_details, name="ticket-details"),
    path("create/", views.create_ticket, name="create-ticket"),
]
