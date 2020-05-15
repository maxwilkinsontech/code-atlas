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
        response = self.client.get('/search/')
        
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('search'))

        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('search'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    def test_get_search_query(self):
        request = factory.get(reverse('search') + '?q=test')
        view = self.setup_view(SearchView(), request)

        self.assertEqual(view.get_search_query(), 'test')

    def test_get_queryset_no_query(self):
        request = factory.get(reverse('search'))
        view = self.setup_view(SearchView(), request) 

        self.assertIsNone(view.get_queryset())

    # TODO: find why this test is not working as expected
    # def test_get_queryset_create_search_history(self):
    #     history_count = SearchHistory.objects.filter(user=self.user).count()
    #     request = factory.get(reverse('search') + '?q=test')
    #     request.user = self.user
    #     view = self.setup_view(SearchView(), request) 

    #     new_history_count = SearchHistory.objects.filter(user=self.user).count()
    #     self.assertEqual(history_count+1, new_history_count)

    def test_get_queryset_with_query(self):
        for i in range(10):
            Note.objects.create(user=self.user, title='test', content='test')

        request = factory.get(reverse('search') + '?q=test')
        request.user = self.user
        view = self.setup_view(SearchView(), request)

        self.assertEqual(view.get_queryset().count(), 10)

    def test_get_search_history(self):
        SearchHistory.objects.create(user=self.user, query='1')
        SearchHistory.objects.create(user=self.user, query='2')
        SearchHistory.objects.create(user=self.user, query='3')

        request = factory.get(reverse('search') + '?q=test')
        request.user = self.user
        view = self.setup_view(SearchView(), request) 

        self.assertEqual(view.get_search_history().count(), 3)

    def test_get_django_search_results_no_query(self):
        request = factory.get(reverse('search'))
        view = self.setup_view(SearchView(), request) 

        self.assertEqual(view.get_django_search_results(), [])

    def test_get_django_search_results_query_present(self):
        request = factory.get(reverse('search') + '?q=test')
        view = self.setup_view(SearchView(), request) 

        self.assertNotEqual(len(view.get_django_search_results()), 0)

    def test_django_doc_info(self):
        request = factory.get(reverse('search') + '?q=test')
        view = self.setup_view(SearchView(), request) 

        info = view.django_doc_info()

        self.assertIsNotNone(info.get('url'))
        self.assertIsNotNone(info.get('version'))