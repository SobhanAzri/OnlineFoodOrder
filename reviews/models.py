
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import CustomUser
from restaurants.models import FoodItem


class Review(models.Model):

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Customer who wrote the review.",
    )
    food_item = models.ForeignKey(
        FoodItem,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Food item being reviewed.",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Star rating from 1 (worst) to 5 (best).",
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "food_item"],
                name="unique_review_per_customer_food_item",
            )
        ]

    def __str__(self):
        return (
            f"{self.food_item.name} - {self.rating}/5 "
            f"by {self.customer.username}"
        )
