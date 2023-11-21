from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("details/<int:pk>", views.ticket_details, name="ticket-details"),
]
