from django.test import TestCase, RequestFactory
from django.urls import reverse

from search.models import SearchHistory
from search.views import SearchView
from notes.models import Note
from users.models import User


factory = RequestFactory()

class SearchViewTest(TestCase):
    def setup_view(self, view, request, *args, **kwargs):
        """
        Mimic ``as_view()``, but returns view instance.
        Use this function to get view instances on which you can run unit tests,
        by testing specific methods.
        """
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

        user2 = User.objects.create_user(email='test2@email.com')

        for i in range(10):
            note = Note.objects.create(
                title=i, 
                content=f'some words for testing {i}', 
                user=self.user
            )

        for i in range(10, 20):
            note = Note.objects.create(
                title=i, 
                content=f'some words for testing {i}', 
                user=user2
            )

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
        response = self.client.get((reverse('search') + '?q=test'))

        self.assertEqual(len(response.context['object_list']), 10)

    def test_get_public_notes_with_valid_query(self):
        request = factory.get(reverse('search') + '?q=test')
        request.user = self.user
        view = self.setup_view(SearchView(), request)

        queryset = view.get_public_notes()

        self.assertEqual(queryset.count(), 10)