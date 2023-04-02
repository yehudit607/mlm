from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .exceptions import CheckoutException, checkout_exception
from .schema import CheckoutCreateSchema, CheckoutReturnSchema
from .serializer import CheckoutSerializer
from .service import CheckoutService
from ..permissions.permissions import is_logged_in


@csrf_exempt
@api_view(["GET"])
def my_checkouts(request):
    try:
        user = request.user
        checkouts = CheckoutService.get_checkouts(user)
        return Response(CheckoutSerializer(checkouts, many=True).data, status=status.HTTP_200_OK)
    except CheckoutException as ex:
        return checkout_exception(ex)


@csrf_exempt
@is_logged_in
@api_view(["POST"])
def checkout(request):
    schema = CheckoutCreateSchema(data=request.data)
    schema.is_valid(raise_exception=True)
    user = request.user
    book_id = schema.validated_data.get('book_id')
    checkout = CheckoutService.checkout_book(user, book_id)
    return Response(CheckoutSerializer(checkout).data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(["POST"])
def return_book(request):
    serializer = CheckoutReturnSchema(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = request.user
    checkout_id = serializer.validated_data.get('checkout_id')
    checkout = CheckoutService.return_book(user, checkout_id)
    return Response(CheckoutSerializer(checkout).data, status=status.HTTP_200_OK)
