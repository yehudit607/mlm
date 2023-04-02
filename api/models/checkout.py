from django.db import models


class Checkout(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        "api.User",
        on_delete=models.CASCADE,
        related_name="checkouts",
        null=True,
        blank=True,
    )

    book = models.ForeignKey(
        "api.Book",
        on_delete=models.CASCADE,
        related_name="checkouts",
        null=True,
        blank=True,
    )
    checkout_date = models.DateTimeField(null=True, default=None)
    returned = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, default=None)
    return_date = models.DateTimeField(null=True, default=None)

