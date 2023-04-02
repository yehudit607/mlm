from rest_framework import serializers

from api.models.book import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id',
                  'title',
                  'author',
                  'publication_year',
                  'available_copies',
                  'total_copies',
                  'isbn',
                  'description')
