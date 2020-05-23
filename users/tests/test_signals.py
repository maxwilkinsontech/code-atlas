from django.test import TestCase

from users.models import User


class SetupUserAccountSignalTest(TestCase):
    def test_user_preferences_model_create(self):
        user = User.objects.create_user(email='test@email.com')

        self.assertIsNotNone(user.preferences)