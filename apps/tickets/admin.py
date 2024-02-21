from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Ticket, TicketAttachment, TicketComment


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment


class TicketAdmin(SimpleHistoryAdmin):
    inlines = [
        TicketAttachmentInline,
    ]

    def save_model(self, request, obj, form, change):
        obj._change_reason = "Ticket has been modified by Admin."
        print("TicketAdmin")
        print("Form", form)
        return super(TicketAdmin, self).save_model(request, obj, form, change)


# Register your models here.
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketComment)
admin.site.register(TicketAttachment)
