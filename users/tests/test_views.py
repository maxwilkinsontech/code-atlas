from django.test import TestCase
from django.urls import reverse

from users.models import User


class SettingsTest(TestCase):
    def setUp(self):
        # Login User
        self.user = User.objects.create_user(email='test@email.com')
        psw = 'password'
        self.user.set_password(psw)
        self.user.save()
        self.client.login(
            email=self.user.email, 
            password=psw
        )

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

    def test_view_url_change_email(self):
        email = 'test2@email.com'
        response = self.client.post(
            reverse('account_settings'),
            data={
                'email': email
            }    
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, email)

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
                'password': 'dfhsdjhHJKHJASHdfh3434'
            }    
        )
        self.assertEqual(response.status_code, 302)    

class DeleteAccountTest(TestCase):        
    def test_delete(self):
        email = 'test123@email.com'
        user = User.objects.create_user(email=email)
        response = self.client.post(reverse('delete_account', args=[email]))

        self.assertEqual(response.status_code, 302)

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

    def test_post_successful(self):
        email = 'new_user@email.com'
        response = self.client.post(
            reverse('signup'),
            data={
                'email': email,
                'password1': 'sdDsd34cvc',
                'password2': 'sdDsd34cvc',
            }    
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email=email).exists())

    def test_post_user_already_exists(self):
        User.objects.create_user(email='test@email.com')

        response = self.client.post(
            reverse('signup'),
            data={
                'email': 'test@email.com',
                'password1': 'password',
                'password2': 'password',
            }    
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['form'].errors, '')
        
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
        # Login User
        self.user = User.objects.create_user(email='test@email.com')
        psw = 'password'
        self.user.set_password(psw)
        self.user.save()
        self.client.login(
            email=self.user.email, 
            password=psw
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/logout/')
        
        self.assertEqual(response.status_code, 302)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 302)
    
