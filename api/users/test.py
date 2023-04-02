from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import User


class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('user_create')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')
