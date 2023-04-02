from rest_framework import serializers
from mlm.api.models.checkout import Checkout


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ('id', 'user', 'book', 'checkout_date', 'due_date', 'returned', 'return_date')
