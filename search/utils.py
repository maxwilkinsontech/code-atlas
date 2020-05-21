import re

from django.contrib.postgres.search import SearchRank
from django.db.models import F

from tagging.models import TaggedItem

from .models import SearchHistory
from notes.models import Note


class SearchUtil:
    """
    Class providing implementation for Note searching. Can search a User's Notes or for any public 
    Notes.
    """
    def __init__(self, search_query, user=None, ordering=['-rank'], 
                 fields=['id', 'title', 'content'], log=True):
        """
        `log`: indicates if the search query should be logged for the given User. Also indicates if 
        the given User's Notes should be included.
        """
        self.ordering = ordering
        self.fields = fields
        self.log = log
        # query data
        query, tags = self.parse_search_query(search_query)
        self.query = query
        self.tags = tags
        self.user = user
        self.queryset = self.get_queryset()

    def parse_search_query(self, search_query):
        """
        Extract infomation from search query. User's can use predefined syntax to filter their 
        search. A search query could look like: @tag_name @"tag name" search query
        The syntax for filter by a tag is @. Double quotations can be used to input a multi-word 
        tag.
        """
        tags = []
        def replacer(match):
            tags.append(match.group(2))
            return ""

        search_query = re.sub(r'@(")?((?(1)[^"]+|\w+))(?(1)")', replacer, search_query)
        search_query = re.sub(r'\s+', ' ', search_query).strip()

        return search_query, tags

    def get_queryset(self):
        """
        Return a Note queryset. If `user` is not None, return the given User's Notes otherwise 
        return than all Notes. If `log` is False, only return Notes not created by User.
        """
        queryset = Note.objects.all()
        if self.user: 
            if self.log:
                queryset = queryset.filter(user=self.user)
            else:
                queryset = queryset.exclude(user=self.user).filter(is_public=True)

        return queryset

    def log_search(self):
        """
        Make a log of the search query for the given User.
        """
        if self.user and self.log:
            SearchHistory.objects.create(
                user=self.user, 
                query=self.query
            )

    def get_search_results(self):
        """
        Call chained search methods. Returns queryset. Queryset is not evaluated.
        """
        self.log_search()
        queryset = (
            self.filter_query()
                .filter_tags()
                .order_queryset()
                .select_fields()
        ).queryset

        return queryset

    def filter_query(self):
        """
        Filter the queryset against the query. If the query is empty, then only tags are in the 
        search query. Skip this step.
        """
        query = self.query
        queryset = self.queryset
        
        if query:
            queryset = queryset.filter(
                document_vector=query
            ).annotate(
                rank=SearchRank('document_vector', query),
            )
        else:
            queryset = queryset.annotate(
                rank=F('last_edited'),
            )

        self.queryset = queryset
        return self

    def filter_tags(self):
        """
        Given a list of tags, return a filtered queryset of the given User's Note objects with tags 
        in the given tags.
        """
        tags = self.tags

        if tags:
            queryset = TaggedItem.objects.get_intersection_by_model(self.queryset, tags)
            self.queryset = queryset

        return self

    def order_queryset(self):
        """
        Order the queryset by the parameters initialised with.
        """
        queryset = self.queryset.order_by(*self.ordering)
        self.queryset = queryset

        return self

    def select_fields(self):
        """
        Define the fields of the model to be selected.
        """
        queryset = self.queryset.values(*self.fields)
        self.queryset = queryset

        return self