"""Admin registrations for the ``restaurants`` app."""

from django.contrib import admin

from .models import FoodItem, Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """Admin configuration for restaurants."""

    list_display = (
        "name",
        "owner",
        "is_active",
        "location_lat",
        "location_lng",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "address")


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    """Admin configuration for food items."""

    list_display = ("name", "restaurant", "price", "is_available")
    list_filter = ("is_available", "restaurant")
    search_fields = ("name", "restaurant__name")
