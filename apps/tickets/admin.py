from django.contrib import admin

from .models import Ticket, TicketComment, TicketPriority, TicketStatus, TicketType

# Register your models here.
admin.site.register(Ticket)
admin.site.register(TicketType)
admin.site.register(TicketStatus)
admin.site.register(TicketComment)
admin.site.register(TicketPriority)
