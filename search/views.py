from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .utils import SearchUtil


class SearchView(LoginRequiredMixin, ListView):
    """
    Search and return a list Note objects. Search query queries against Note title.
    """
    template_name = 'search.html'
    paginate_by = 12

    def get_queryset(self):
        """
        If there is a search_query present in the url, search the given User's Notes. Make a log of
        the search query for the User.
        """
        search_query = self.request.GET.get('q', '')
        if search_query:
            user = self.request.user
            search_util = SearchUtil(search_query, user=user)
            results = search_util.get_search_results()
            return results
        return []