"""Models and custom managers for the ``orders`` app."""

from django.db import models
from django.utils import timezone

from accounts.models import CustomUser
from restaurants.models import FoodItem, Restaurant


class ActiveDiscountManager(models.Manager):

    def get_valid_discounts(self):

        now = timezone.now()
        return self.get_queryset().filter(
            is_active=True,
            valid_from__lte=now,
            valid_to__gte=now,
        )


class Discount(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="discounts",
        help_text="Restaurant that offers this discount code.",
    )
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.IntegerField(
        help_text="Percentage of the total price to remove (0-100).",
    )
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveDiscountManager()

    class Meta:
        """Model metadata."""

        verbose_name = "Discount"
        verbose_name_plural = "Discounts"
        ordering = ["-valid_from"]

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"


class Order(models.Model):

    class Status(models.TextChoices):

        PENDING = "Pending", "Pending"
        PREPARING = "Preparing", "Preparing"
        SENT = "Sent", "Sent"
        DELIVERED = "Delivered", "Delivered"
        CANCELED = "Canceled", "Canceled"

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="orders",
        help_text="User who placed the order.",
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="orders",
        help_text="Restaurant the order was placed at.",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        help_text="Optional discount code applied to this order.",
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Model metadata."""

        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.customer.username} ({self.status})"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        help_text="Order this line belongs to.",
    )
    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.PROTECT,
        related_name="order_items",
        help_text="Food item that was ordered.",
    )
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Unit price of the food item at the moment of ordering.",
    )

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["order", "food_item"]

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"


class Cart(models.Model):

    customer = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="cart",
        help_text="Customer who owns this cart.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Cart of {self.customer.username}"


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        help_text="Cart this line belongs to.",
    )
    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE,
        related_name="cart_items",
        help_text="Food item added to the cart.",
    )
    quantity = models.PositiveIntegerField()

    class Meta:

        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        ordering = ["cart", "food_item"]

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"
