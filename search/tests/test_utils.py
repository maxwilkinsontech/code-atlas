from django.test import TestCase

from search.utils import search_django_site, django_docs_info


class UtilsTest(TestCase):
    def test_search_django_site_valid_results(self):
        """Test that the scraping results results with a known correct query"""
        results = search_django_site('test')

        self.assertNotEqual(len(results), 0)

    def test_search_django_site_no_results(self):
        """Test that the scraping results results with a know incorrect query"""
        results = search_django_site('tadfsdfk3h4rwhfjkhdjkfbkh23ui ghhsbdest')

        self.assertEqual(results, [])

    def test_search_django_site_empty_query(self):
        """Test that the scraping results results with a know incorrect query"""
        results = search_django_site('')

        self.assertEqual(results, [])

    def test_django_docs_info(self):
        info = django_docs_info()
        
        self.assertTrue('url' in info)
        self.assertTrue('version' in info)
