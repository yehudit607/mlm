import os
from django.urls import reverse
from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from rest_framework import status

from api.models import User


class UserTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mlm.settings')
        setup_test_environment()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.client = Client()

    def test_create_user(self):
        url = reverse('user_create')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')
