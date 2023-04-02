from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view
from rest_framework import status

from api.models import User
from mlm.settings import LOGIN_RATE_LIMIT


def get_limit_key(data_key, request):
    data = request.data if hasattr(request, "data") else {}
    by_data = data.get(data_key, data_key).strip()
    limit_key = f"{request.path}_{by_data}"
    return limit_key


def limit_by(data_key):
    def limiter(group, request):
        return get_limit_key(data_key, request)

    return limiter


limit_by_username = limit_by("username")
limit_by_email = limit_by("email")


@api_view(["POST"])
@ratelimit(key=limit_by_username, rate=f"{LOGIN_RATE_LIMIT}/m", method='POST', block=True)
def login_view(request):
    payload = request.data

    email = payload.get("email", "").strip()
    password = payload.get("password")

    try:
        unauthenticated_user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return JsonResponse({"error": "wrong credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    authenticated_user = authenticate(request, username=unauthenticated_user.username, password=password)

    if not authenticated_user or not authenticated_user.is_active:
        return JsonResponse({"error": "wrong credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    login(request, authenticated_user)

    response_data = {
        "email": email,
        "date_joined": authenticated_user.date_joined,
    }

    return JsonResponse(response_data, status=status.HTTP_200_OK)
