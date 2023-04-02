from django.contrib.auth.models import AbstractUser
from django.db import models

from api.infra import utils


class User(AbstractUser):

    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    @property
    def display_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.display_name} ({self.id})"

    @property
    def active_checkouts(self):
        return self.checkouts.filter(returned=False)


def create_username(email):
    return f"{utils.generate_random(10)}_{email}"