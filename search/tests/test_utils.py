from django.test import TestCase

from search.utils import SearchUtil


class SearchUtilTest(TestCase):
    def test_parse_search_query(self):
        t1 = SearchUtil()
