from rest_framework import serializers


class BookCreateSchema(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1)
    author = serializers.CharField(required=True)
    publication_year = serializers.CharField(required=False, allow_blank=True)
    total_copies = serializers.IntegerField(required=False)
    isbn = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)


class BookUpdateSchema(serializers.Serializer):
    title = serializers.CharField(required=False, min_length=1)
    author = serializers.CharField(required=False, allow_blank=True)
    publication_year = serializers.CharField(required=False)
    available_copies = serializers.IntegerField(required=False)
    total_copies = serializers.IntegerField(required=False)
    isbn = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)