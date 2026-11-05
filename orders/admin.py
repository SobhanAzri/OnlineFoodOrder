"""Admin registrations for the ``orders`` app."""

from django.contrib import admin

from .models import Cart, CartItem, Discount, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Show order lines inline with their order."""

    model = OrderItem
    extra = 0


class CartItemInline(admin.TabularInline):
    """Show cart lines inline with their cart."""

    model = CartItem
    extra = 0


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Admin configuration for discount codes."""

    list_display = (
        "code",
        "restaurant",
        "discount_percent",
        "valid_from",
        "valid_to",
        "is_active",
    )
    list_filter = ("is_active", "restaurant")
    search_fields = ("code",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for orders."""

    list_display = (
        "id",
        "customer",
        "restaurant",
        "status",
        "total_price",
        "created_at",
    )
    list_filter = ("status", "restaurant")
    search_fields = ("customer__username",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin configuration for order line items."""

    list_display = ("order", "food_item", "quantity", "price_at_order")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin configuration for carts."""

    list_display = ("customer", "created_at")
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin configuration for cart line items."""

    list_display = ("cart", "food_item", "quantity")
