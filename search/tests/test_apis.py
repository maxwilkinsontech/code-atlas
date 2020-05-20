from django.test import TestCase
from django.urls import reverse

from search.models import SearchHistory
from search.views import SearchView
from notes.models import Note
from users.models import User


class SearchPublicNotesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()

        note = Note.objects.create(
            title=1, 
            content=f'some words for testing 1', 
            user=self.user
        )

        user2 = User.objects.create_user(email='test2@email.com')
        Note.objects.create(
            title=2, 
            content=f'some words for testing 2', 
            user=user2
        )

    def test_request_authenticated(self):
        response = self.client.get(reverse('api_search_public_notes'))
        
        self.assertEqual(response.status_code, 403)

    def test_no_query_passed(self):
        self.client.login(email=self.user.email, password='password')        
        response = self.client.get(reverse('api_search_public_notes'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])

    def test_no_results_found(self):
        self.client.login(email=self.user.email, password='password')        
        response = self.client.get(reverse('api_search_public_notes') + '?q=1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])

    def test_results_found(self):
        self.client.login(email=self.user.email, password='password')        
        response = self.client.get(reverse('api_search_public_notes') + '?q=2')
        
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['results'], [])