from django.db import models


class Book(models.Model):

    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    publication_year = models.IntegerField(null=True, blank=True)
    available_copies = models.IntegerField(null=True, default=1)
    total_copies = models.IntegerField(default=1)
    isbn = models.CharField(null=True, blank=True, max_length=1024)
    description = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.author} ({self.id})"

