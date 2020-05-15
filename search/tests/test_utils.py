from django.test import TestCase

from search.utils import search_django_site


class UtilsTest(TestCase):
    def test_search_django_site(self):
        """Test that the scraping results results with a know correct query"""
        results = search_django_site('test')

        self.assertNotEqual(len(results), 0)