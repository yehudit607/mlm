from typing import List
from api.models import Checkout, Book
from django.core.exceptions import ObjectDoesNotExist


class CheckoutService:

    @staticmethod
    def get_checkouts(user):
        return user.active_checkouts

    @staticmethod
    def checkout_book(user, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            if book.available_copies <= 0:
                raise Exception("Book is not available")
            book.available_copies -= 1
            book.save()
            checkout = Checkout(user=user, book=book)
            checkout.save()
            return checkout
        except ObjectDoesNotExist:
            raise Exception("Book not found")

    @staticmethod
    def return_book(user, checkout_id):
        try:
            checkout = Checkout.objects.get(pk=checkout_id, user=user)
            if checkout.returned:
                raise Exception("Book already returned")
            checkout.book.available_copies += 1
            checkout.book.save()
            checkout.returned = True
            checkout.save()
            return checkout
        except ObjectDoesNotExist:
            raise Exception("Checkout not found")
