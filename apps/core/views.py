from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, render

from ..users.models import User


@login_required
def dashboard(request):
    users = User.objects.all()
    context = {"users": users, "current_user": request.user, "page": "dashboard"}
    return render(request=request, template_name="core/dashboard.html", context=context)
