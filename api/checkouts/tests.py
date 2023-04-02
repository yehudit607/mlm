from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Checkout, Book, User


class CheckoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='userpassword'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890',
            stock=10
        )

    def test_checkout_book(self):
        self.client.login(email='user@example.com', password='userpassword')
        url = reverse('checkout')
        data = {
            'book_id': self.book.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Checkout.objects.count(), 1)

