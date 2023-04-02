from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Book, User


class BookTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword'
        )
        self.non_admin = User.objects.create_user(
            email='nonadmin@example.com',
            password='nonadminpassword'
        )

    def test_add_book_by_admin(self):
        self.client.login(email='admin@example.com', password='adminpassword')
        url = reverse('book_list_create')
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890',
            'stock': 10
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book')

    def test_add_book_by_non_admin(self):
        self.client.login(email='nonadmin@example.com', password='nonadminpassword')
        url = reverse('book_list_create')
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890',
            'stock': 10
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
