from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from .utils import SearchUtil
from notes.serializers import NoteSerializer


class SearchPublicNotesView(ListAPIView):
    """
    Returns public Notes matching query.
    """
    serializer_class = NoteSerializer
    # permission_classes = [IsAuthenticated]
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            user = self.request.user
            search_util = SearchUtil(search_query, user=user, log=False)
            results = search_util.get_search_results()
            # TODO: check for multiple queries
            print(results.count())
            return results
        return []
