
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    is_customer = models.BooleanField(
        default=True,
        help_text="Marks the user as a customer that can place orders.",
    )
    is_restaurant_owner = models.BooleanField(
        default=False,
        help_text="Marks the user as an owner who can manage restaurants.",
    )

    class Meta:

        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["username"]

    def __str__(self):
        return self.username


class CustomerProfile(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="customer_profile",
        help_text="The user account this customer profile belongs to.",
    )
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    location_lat = models.FloatField(null=True, blank=True)
    location_lng = models.FloatField(null=True, blank=True)

    class Meta:

        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"
        ordering = ["user__username"]

    def __str__(self):
        return f"Customer profile of {self.user.username}"


class RestaurantOwnerProfile(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="owner_profile",
        help_text="The user account this owner profile belongs to.",
    )
    phone_number = models.CharField(max_length=20)

    class Meta:

        verbose_name = "Restaurant Owner Profile"
        verbose_name_plural = "Restaurant Owner Profiles"
        ordering = ["user__username"]

    def __str__(self):
        return f"Owner profile of {self.user.username}"
