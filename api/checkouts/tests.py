from django.test import TestCase

from api.models import User, Book, Checkout


class CheckoutModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890',
            stock=10
        )

    def test_create_checkout(self):
        checkout = Checkout.objects.create(
            user=self.user,
            book=self.book,
            due_date='2023-04-15'
        )
        self.assertEqual(checkout.user, self.user)
        self.assertEqual(checkout.book, self.book)
