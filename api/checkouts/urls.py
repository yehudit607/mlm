from django.urls import path
from .views import my_checkouts, checkout, return_book

urlpatterns = [
    path("/my-checkouts", my_checkouts, name="my_checkouts"),
    path("/checkout", checkout, name="checkout"),
    path("/return", return_book, name="return_book"),
]

