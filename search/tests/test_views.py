from django.test import TestCase
from django.urls import reverse

from search.models import SearchHistory
from search.views import SearchView
from notes.models import Note
from users.models import User


class SearchViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/search/')
        
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('search'))

        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('search'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_view_get_queryset_no_query(self):
        response = self.client.get(reverse('search'))

        self.assertEqual(response.context['object_list'], [])    

    def test_get_queryset_with_valid_query(self):
        for i in range(24):
            Note.objects.create(user=self.user, title='test', content='test')

        response = self.client.get((reverse('search') + '?q=test'))

        self.assertNotEqual(response.context['object_list'], [])