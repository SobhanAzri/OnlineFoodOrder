"""Admin registrations for the ``reviews`` app."""

from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for reviews."""

    list_display = ("food_item", "customer", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("food_item__name", "customer__username")
