from django.contrib import admin

from .models import Department, User, UserRole

# Register your models here.
admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(Department)
