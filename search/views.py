from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .utils import django_docs_info, search_django_site, SearchUtil
from .models import SearchHistory


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
        If there is a search_query present in the url, search the given User's Notes. Make a log of
        the search query for the User.
        """
        search_query = self.get_search_query()
        if search_query is not None:
            user = self.request.user
            SearchHistory.objects.create(user=user, query=search_query)
            search_util = SearchUtil(search_query, user=user)
            results = search_util.get_search_results()

            return results
        return