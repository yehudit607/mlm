from django.http import JsonResponse
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_admin)


class IsAdminUserOrReadOnly(BasePermission):
    """
    Allows access only to admin users to put post delete and all users to get
    """

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (request.user.is_admin or request.method in SAFE_METHODS)
        )


def is_logged_in(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)

        return JsonResponse({"error": "wrong credentials"}, status=403)

    return wrapper