from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .utils import django_docs_info, search_django_site
from .models import SearchHistory
from notes.models import Note


class SearchView(LoginRequiredMixin, ListView):
    """
    Search and return a list Note objects. Search query queries against Note title.
    """
    template_name = 'search.html'

    def get_search_query(self):
        """
        Get and return the search query in the url name `q`.
        """
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        """
        Add Django documentation to context.
        """
        data = super().get_context_data(**kwargs)
        search_query = self.get_search_query()
        # Add Django documentation results
        data['django_search_results'] = search_django_site(search_query)
        data['django_docs_info'] = django_docs_info()
        return data

    def get_queryset(self):
        """
        Get the User's Notes ordered by ranking with given search query. Implements a full-text
        search on the fields: `title` and `content`.
        """
        search_query = self.get_search_query()
        if search_query is not None:
            user = self.request.user
            # Log search query.
            SearchHistory.objects.create(user=self.request.user, query=search_query)
            # Return search results
            vector = SearchVector('title', 'content')
            query = SearchQuery(search_query)
            results = Note.objects.filter(user=user).annotate(rank=SearchRank(vector, query)).order_by('-rank')[:12]
            return results
        return