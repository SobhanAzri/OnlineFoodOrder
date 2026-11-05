"""Admin registrations for the ``core`` app."""

from django.contrib import admin

from .models import NotificationLog


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    """Admin configuration for notification logs."""

    list_display = ("user", "notification_type", "is_sent", "created_at")
    list_filter = ("notification_type", "is_sent")
    search_fields = ("user__username", "message")
