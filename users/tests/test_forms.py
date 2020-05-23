from django.test import TestCase, RequestFactory
from django.urls import reverse

from users.forms import SettingsForm, SignUpForm, SetUsernameForm
from users.models import User


factory = RequestFactory()

class SignUpFormTest(TestCase):
    def test_form_with_one_password(self):
        form_data = {'email': 'test@email.com', 'password1': 'password'}
        form = SignUpForm(data=form_data)
        form.is_valid()
        user = form.save()

        self.assertIsNotNone(user)

class SetUsernameFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')

    def test_clean_with_valid_username(self):
        form_data = {'username': 'newusername'}

        form = SetUsernameForm(data=form_data, user=self.user)
        form.is_valid()
        form.clean()

        self.assertEqual(form.errors, {})

    def test_clean_with_invalid_username(self):
        User.objects.create_user(email='test2@email.com')
        form_data = {'username': 'test2'}

        form = SetUsernameForm(data=form_data, user=self.user)
        form.is_valid()
        form.clean()

        self.assertNotEqual(form.errors, {})

    def test_save(self):
        username = 'newusername'
        form_data = {'username': username, 'email_consent': 'on'}

        form = SetUsernameForm(data=form_data, user=self.user)
        form.is_valid()
        form.clean()
        form.save('on')

        self.assertEqual(self.user.username, username)
        self.assertEqual(self.user.preferences.email_consent, True)

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

    def test_clean_with_valid_username_email(self):
        form_data = {'username': 'test', 'email': 'test2@email.com'}

        form = SettingsForm(data=form_data, user=self.user, request=self.request)
        form.is_valid()
        form.clean()

        self.assertEqual(form.errors, {})

    def test_save_all_empty_string(self):
        form_data = {'username': '', 'email': '', 'password': ''}

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

    def test_save_username(self):
        form_data = {'username': 'newusername'}

        form = SettingsForm(data=form_data, user=self.user, request=self.request)
        form.is_valid()
        
        user = form.save()

        self.assertEqual(user.username, 'newusername')

    