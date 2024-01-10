from django.contrib import admin

from .models import Ticket, TicketAttachment, TicketComment


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment


class TicketAdmin(admin.ModelAdmin):
    inlines = [
        TicketAttachmentInline,
    ]


# Register your models here.
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketComment)
admin.site.register(TicketAttachment)
