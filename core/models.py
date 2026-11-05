from django.conf import settings
from django.db import models


class NotificationLog(models.Model):
    """Placeholder record of an email or SMS notification."""

    class NotificationType(models.TextChoices):
        """Channels a notification can be delivered through."""

        EMAIL = "Email", "Email"
        SMS = "SMS", "SMS"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text="User who should receive the notification.",
    )
    message = models.TextField()
    notification_type = models.CharField(
        max_length=10,
        choices=NotificationType.choices,
        default=NotificationType.EMAIL,
    )
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model metadata."""

        verbose_name = "Notification Log"
        verbose_name_plural = "Notification Logs"
        ordering = ["-created_at"]

    def __str__(self):
        """Return the channel, recipient and delivery state."""
        state = "sent" if self.is_sent else "pending"
        return f"{self.notification_type} to {self.user.username} ({state})"
