"""Admin registrations for the ``accounts`` app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, CustomerProfile, RestaurantOwnerProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin configuration that surfaces the custom role flags."""

    list_display = (
        "username",
        "email",
        "is_customer",
        "is_restaurant_owner",
        "is_staff",
    )
    list_filter = (
        "is_customer",
        "is_restaurant_owner",
        "is_staff",
        "is_superuser",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Food Ordering Roles",
            {"fields": ("is_customer", "is_restaurant_owner")},
        ),
    )


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    """Admin configuration for customer profiles."""

    list_display = ("user", "phone_number", "location_lat", "location_lng")
    search_fields = ("user__username", "phone_number")


@admin.register(RestaurantOwnerProfile)
class RestaurantOwnerProfileAdmin(admin.ModelAdmin):
    """Admin configuration for restaurant owner profiles."""

    list_display = ("user", "phone_number")
    search_fields = ("user__username", "phone_number")
