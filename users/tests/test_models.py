from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='test@email.com')

        self.assertIsNotNone(user)

    def test_create_superuser(self):
        user = User.objects.create_user(email='test2@email.com')

        self.assertIsNotNone(user)