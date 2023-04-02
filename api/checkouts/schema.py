from rest_framework import serializers


class CheckoutCreateSchema(serializers.Serializer):
    book_id = serializers.IntegerField(required=True)


class CheckoutReturnSchema(serializers.Serializer):
    checkout_id = serializers.IntegerField(required=True)
