from django.test import TestCase
from django.urls import reverse

from users.models import User


class SettingsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/settings/')
        
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('account_settings'))

        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('account_settings'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')

    def test_preferences_form_in_context(self):
        response = self.client.get(reverse('account_settings'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('preferences_form' in response.context)

    def test_view_url_change_email(self):
        email = 'test2@email.com'
        username = 'new_username'
        response = self.client.post(
            reverse('account_settings'),
            data={
                'email': email,
                'username': username
            }    
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, email)
        self.assertEqual(self.user.username, username)

    def test_view_url_change_email_fail(self):
        email = 'existing@email.com'
        User.objects.create(email=email)
        response = self.client.post(
            reverse('account_settings'),
            data={
                'email': email
            }    
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['form'].errors, '')

    def test_view_url_change_password(self):
        response = self.client.post(
            reverse('account_settings'),
            data={
                'email': self.user.email,
                'username': self.user.username,
                'password': 'dfhsdjhHJKHJASHdfh3434'
            }    
        )
        self.assertEqual(response.status_code, 302)    

class DeleteAccountTest(TestCase):        
    def test_delete(self):
        email = 'test123@email.com'
        user = User.objects.create_user(email=email)
        user.set_password('password')
        user.save()
        self.client.login(email=email, password='password')
        response = self.client.post(reverse('delete_account'))

        self.assertEqual(response.status_code, 302)
        delete_user = User.objects.filter(email=email)
        self.assertFalse(delete_user.exists())

class SignUpTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/signup/')
        
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('signup'))

        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

class SetUsernameViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/signup/username/')
        
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('set_username'))

        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('set_username'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'set_username.html')
    
    def test_dispatcg(self):
        preferences = self.user.preferences
        preferences.email_consent = True
        preferences.save()
        response = self.client.get(reverse('set_username'))

        self.assertEqual(response.status_code, 302)

    def test_post(self):
        response = self.client.post(
            reverse('set_username'),
            data={
                'username': 'new_username',
                'email_content': 'off'
            }    
        )

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.username, 'new_username')
        self.assertEqual(self.user.preferences.email_consent, False)
        
class SignInTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/signin/')
        
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')
        
class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/logout/')
        
        self.assertEqual(response.status_code, 302)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 302)