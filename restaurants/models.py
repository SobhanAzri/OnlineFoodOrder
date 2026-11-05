
from django.db import models

from accounts.models import RestaurantOwnerProfile


class ActiveRestaurantManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Restaurant(models.Model):
    owner = models.ForeignKey(
        RestaurantOwnerProfile,
        on_delete=models.CASCADE,
        related_name="restaurants",
        help_text="Owner profile responsible for this restaurant.",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.TextField()
    location_lat = models.FloatField(null=True, blank=True)
    location_lng = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active_objects = ActiveRestaurantManager()

    class Meta:

        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
        ordering = ["name"]

    def __str__(self):
        return self.name


class AvailableFoodManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)


class FoodItem(models.Model):

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="menu",
        help_text="Restaurant this food item belongs to.",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="food_images/")
    is_available = models.BooleanField(default=True)

    objects = models.Manager()
    available_objects = AvailableFoodManager()

    class Meta:
        verbose_name = "Food Item"
        verbose_name_plural = "Food Items"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"
