from django.test import TestCase

from users.models import User
from search.models import SearchHistory


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='test@email.com')

        self.assertIsNotNone(user)

    def test_create_superuser(self):
        user = User.objects.create_user(email='test2@email.com')

        self.assertIsNotNone(user)

    def test_get_recent_searches(self):
        user = User.objects.create_user(email='test3@email.com')

        for i in range(10):
            SearchHistory.objects.create(user=user, query=i)

        searches = user.get_recent_searches()

        self.assertEqual(searches.count(), 5)