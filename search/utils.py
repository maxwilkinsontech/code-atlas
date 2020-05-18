import requests
import re

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F

from tagging.models import TaggedItem
from bs4 import BeautifulSoup

from notes.models import Note


def django_docs_info():
    """
    Return infomation about the version of the Django Documentation being used.
    """
    url = 'https://docs.djangoproject.com/en/3.0/'
    version = 3.0
    return {
        'url': url,
        'version': version
    }

def search_django_site(query):
    """
    Make a request to the Django documentation site, passing the given query. Return the results 
    displayed on the first page.
    """
    DJANGO_ENDPOINT = 'https://docs.djangoproject.com/en/3.0/search/'
    final_results = []

    if query == '':
        return final_results
    
    response = requests.get(DJANGO_ENDPOINT, params={'q': query})

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        results_list = soup.find('dl', class_='search-links')
        if results_list is not None:
            results = results_list.findAll('dt')
            for result in results:
                title_anchor = result.find('h2', class_='result-title').find('a')
                title = title_anchor.text.strip()
                url = title_anchor['href']
                
                breadcrumbs = []
                for crumb in result.find('span', class_='meta breadcrumbs').findAll('a'):
                    breadcrumbs.append(crumb.text.strip())

                final_results.append({
                    'title': title,
                    'url': url,
                    'breadcrumbs': ' > '.join(breadcrumbs)
                })

    return final_results

# --------------------------------------------------------------------------------------------------
#                                   Utils for searching Notes
# --------------------------------------------------------------------------------------------------
class SearchUtil:
    """
    Class providing implementation for Note searching. Can search a User's Notes or for any public 
    Notes.
    """
    def __init__(self, search_query, user=None, ordering=['-rank'], 
                 fields=['id', 'title', 'content']):
        query, tags = self.parse_search_query(search_query)
        # query data
        self.query = query
        self.tags = tags
        self.user = user
        self.queryset = self.get_queryset(user)
        # class settings
        self.ordering = ordering
        self.fields = fields

    def parse_search_query(self, search_query):
        """
        Extract infomation from search query. User's can use predefined syntax to filter their search. A
        search query could look like: @tag_name @"tag name" search query
        The syntax for filter by a tag is @. Double quotations can be used to input a multi-word tag. 
        The search query is just text.

        NOTE: if you're reading this, please suggest some better regex as I have no idea what I'm
        doing.
        """
        search_query = search_query.lower()
        query = search_query
        tags = []
        # Match single words following an `@` (with no space between)
        pattern_1 = "\B@\w+"
        # Match string (with spaces) between `@"` amd `"`
        pattern_2 = '@"(.*?)"'
        results_1 = re.findall(pattern_1, search_query)
        results_2 = re.findall(pattern_2, search_query)

        for tag in results_1:
            # Matches still have `@` prepended, so remove.
            clean_tag = tag.replace('@', '')
            tags.append(clean_tag)
            # Remove tag from query
            query = query.replace(tag, '')

        for tag in results_2:
            tags.append(tag)
            # Add back the surrounding strings.
            tag = f'@"{tag}"'
            query = query.replace(tag, '')

        return query.strip(), tags

    def get_queryset(self, user):
        """
        Return a Note queryset. If `user` is not None, return the given User's Notes otherwise 
        return than all Notes.
        TODO: index User Notes for faster lookup.
        """
        queryset = Note.objects.all()
        if user is not None:
            queryset = queryset.filter(user=self.user)

        return queryset

    def get_search_results(self):
        """
        Call chained search methods. Returns queryset. Queryset is not evaluated.
        """
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
        # else:
        #     queryset.annotate(rank=F('last_edited'))

        self.queryset = queryset
        return self

    def filter_tags(self):
        """
        Given a list of tags, return a filtered queryset of the given User's Note objects with tags 
        in the given tags.
        """
        tags = self.tags

        if tags:
            queryset = TaggedItem.objects.get_union_by_model(self.queryset, tags)
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