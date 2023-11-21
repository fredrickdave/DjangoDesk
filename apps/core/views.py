from django.shortcuts import HttpResponse, render

from ..users.models import User


# Create your views here.
def index(request):
    users = User.objects.all()
    context = {"users": users, "current_user": request.user}
    return render(request=request, template_name="core/index.html", context=context)
