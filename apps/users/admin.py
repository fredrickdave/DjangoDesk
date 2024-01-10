from django.contrib import admin

from .models import Department, User

# Register your models here.
admin.site.register(User)
admin.site.register(Department)
