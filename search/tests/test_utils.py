from django.test import TestCase

from search.models import SearchHistory
from search.utils import SearchUtil
from users.models import User
from notes.models import Note


class SearchUtilTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        
        for i in range(10):
            note = Note.objects.create(
                title=i, 
                content=f'some words for testing {i}', 
                user=self.user
            )
            note.tags = str(i)
            
    def test_parse_search_query(self):
        """
        Very important test checking that the regex pattern matching is working as it should be. 
        """
        test_queries = [
            {
                'search_query': 'test',
                'expected_query': 'test',
                'expected_tags': []
            },
            {
                'search_query': 'test @tag1',
                'expected_query': 'test',
                'expected_tags': ['tag1']
            },
            {
                'search_query': 'test @"tag multi"',
                'expected_query': 'test',
                'expected_tags': ['tag multi']
            },
            {
                'search_query': 'test @"tag multi" @tag more test',
                'expected_query': 'test more test',
                'expected_tags': ['tag multi', 'tag']
            },
            {
                'search_query': '    test@"tag multi" @tag    more      test',
                'expected_query': 'test more test',
                'expected_tags': ['tag multi', 'tag']
            },
        ]

        for test in test_queries:
            search_util = SearchUtil(test['search_query'])
            query = search_util.query
            tags = search_util.tags 
            
            self.assertEqual(query, test['expected_query'])
            self.assertEqual(tags, test['expected_tags'])

    def test_get_queryset_with_given_user(self):
        search_util = SearchUtil('test', user=self.user)

        results = search_util.get_queryset()

        self.assertEqual(results.count(), 10)

    def test_get_queryset_no_user(self):
        user2 = User.objects.create_user(email='test2@email.com')
        for i in range(10, 20):
            Note.objects.create(
                title=i, 
                content=f'some words for testing {i}', 
                user=user2
            )

        search_util = SearchUtil('test')

        results = search_util.get_queryset()

        self.assertEqual(results.count(), 20)

    def test_log_search_with_given_user(self):
        history_count = self.user.search_history.count()

        search_util = SearchUtil('1', user=self.user)
        search_util.get_search_results()

        new_history_count = self.user.search_history.count()
        self.assertEqual(history_count+1, new_history_count)

    def test_log_search_no_user(self):
        history_count = SearchHistory.objects.count()

        search_util = SearchUtil('1')
        search_util.get_search_results()

        new_history_count = SearchHistory.objects.count()
        self.assertEqual(history_count, new_history_count)

    def test_filter_query_with_non_empty_query(self):
        search_util = SearchUtil('1', user=self.user)
        search_util.filter_query()

        self.assertEqual(search_util.queryset.count(), 1)

    def test_filter_query_with_empty_query(self):
        search_util = SearchUtil('@1', user=self.user)
        search_util.filter_query()

        self.assertEqual(search_util.queryset.count(), 10)

    def test_filter_tags_with_tags_non_empty(self):
        search_util = SearchUtil('1 @1', user=self.user)
        search_util.filter_tags()

        self.assertEqual(search_util.queryset.count(), 1)        

    def test_filter_tags_with_tags_empty(self):
        search_util = SearchUtil('1', user=self.user)
        search_util.filter_tags()

        self.assertEqual(search_util.queryset.count(), 10)        

    def test_order_queryset(self):
        search_util = SearchUtil('1', user=self.user)

        self.assertIsNotNone(search_util.ordering)

    def test_select_fields(self):
        search_util = SearchUtil('1', user=self.user)
        results = search_util.get_search_results()

        fields = list(results.first().keys())

        self.assertEqual(fields, search_util.fields)

    def test_get_search_results(self):
        search_util = SearchUtil('1', user=self.user)
        results = search_util.get_search_results()

        self.assertEqual(results.count(), 1)
