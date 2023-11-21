from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
]
