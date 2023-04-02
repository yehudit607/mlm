from http import HTTPStatus
from django.http import JsonResponse


class CheckoutException(Exception):
    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        super().__init__(message)
        self.status_code = status_code


def checkout_exception(exception: CheckoutException):
    return JsonResponse({"error": str(exception)}, status=exception.status_code)
