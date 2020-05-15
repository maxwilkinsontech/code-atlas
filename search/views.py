from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import ListView

from .utils import search_django_site
from .models import SearchHistory
from notes.models import Note

#TODO: anonymous users
class Search(ListView):
    """
    Search and return a list Note objects. Search query queries against Note title.
    """
    template_name = 'search.html'

    def get_queryset(self):
        """
        Get the User's Notes ordered by ranking with given search query. Implements a full-text
        search on the fields: `title` and `content`
        """
        search_query = self.get_search_query()
        if search_query is not None:
            user = self.request.user
            # Log search query.
            SearchHistory.objects.create(user=user, query=search_query)
            # Search for matching Notes.
            search_django_site(search_query)
            vector = SearchVector('title', 'content')
            query = SearchQuery(search_query)
            results = Note.objects.filter(user=user).annotate(rank=SearchRank(vector, query)).order_by('-rank')[:10]
            return results
        return

    def get_search_query(self):
        """
        Get and return the search query in the url name `q`.
        """
        return self.request.GET.get('q')

    def get_search_history(self):
        """
        Return the 5 most recent searches the User has made.
        """
        history = self.request.user.search_history.order_by('-search_date').values('query')[:5]
        print(history)
        return history

    def get_django_search_results(self):
        """
        Return the results from Django documentation.
        """
        search_query = self.get_search_query()
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
