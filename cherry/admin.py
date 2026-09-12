from django.contrib import admin
from .models import EmailNotification


@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "subject", "sent_at", "is_sent")
    list_filter = ("is_sent", "sent_at")
    search_fields = ("recipient__email", "subject")
    readonly_fields = ("recipient", "subject", "body", "sent_at")
