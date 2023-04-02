from rest_framework import serializers


class UserCreateSchema(serializers.Serializer):
    email = serializers.EmailField(required=True, min_length=3)
    password = serializers.CharField(required=True, min_length=8, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_admin = serializers.BooleanField(required=False)


class UserUpdateSchema(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False, min_length=8, write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    is_admin = serializers.BooleanField(required=False)
