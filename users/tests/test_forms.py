from django.test import TestCase, RequestFactory
from django.urls import reverse

from users.forms import SettingsForm, SignUpForm
from users.models import User


factory = RequestFactory()

class SignUpFormTest(TestCase):
    def test_form_with_one_password(self):
        form_data = {'email': 'test@email.com', 'password1': 'password'}
        form = SignUpForm(data=form_data)
        form.is_valid()
        user = form.save()

        self.assertIsNotNone(user)

class SettingsFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.request = factory.get(reverse('home'))

    def test_clean_with_existing_email(self):
        User.objects.create_user(email='test2@email.com')
        form_data = {'email': 'test2@email.com'}

        form = SettingsForm(data=form_data, user=self.user, request=self.request)
        form.is_valid()
        form.clean()

        self.assertNotEqual(form.errors, {})

    def test_clean_with_valid_email(self):
        form_data = {'email': 'test2@email.com'}

        form = SettingsForm(data=form_data, user=self.user, request=self.request)
        form.is_valid()
        form.clean()

        self.assertEqual(form.errors, {})

    def test_save_both_empty_string(self):
        form_data = {'email': '', 'password': ''}

        form = SettingsForm(data=form_data, user=self.user, request=self.request)
        form.is_valid()
        
        user = form.save()

        self.assertEqual(user.email, self.user.email)
        self.assertTrue(user.check_password('password'))

    def test_save_email(self):
        form_data = {'email': 'new@email.com'}

        form = SettingsForm(data=form_data, user=self.user, request=self.request)
        form.is_valid()
        
        user = form.save()

        self.assertEqual(user.email, 'new@email.com')

    