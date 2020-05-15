from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import ListView

from notes.models import Note
from .utils import search_django_site


class Search(ListView):
    """
    Search and return a list Note objects. Search query queries against Note title.
    """
    template_name = 'search.html'

    def _get_search_query(self):
        """
        Get and return the search query in the url name `q`.
        """
        return self.request.GET.get('q')

    def get_queryset(self):
        """
        Get the User's Notes ordered by ranking with given search query. Implements a full-text
        search on the fields: `title` and `content`
        """
        search_query = self._get_search_query()
        if search_query is not None:
            search_django_site(search_query)
            user = self.request.user
            vector = SearchVector('title', 'content')
            query = SearchQuery(search_query)
            return Note.objects.filter(user=user).annotate(rank=SearchRank(vector, query)).order_by('-rank')[:10]
        return

    def get_django_search_results(self):
        """
        Return the results from Django documentation.
        """
        search_query = self._get_search_query()
        print(search_query)
        if search_query is not None:
            return search_django_site(search_query)
        return 

    def django_search_info(self):
        """
        Method called from template. Used so that url can be easily changed in future if needed.
        Return a dict.
        """
        url = 'https://docs.djangoproject.com/en/3.0/'
        version = 3.0
        return {
            'url': url,
            'version': version
        }
