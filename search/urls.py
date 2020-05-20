from django.urls import path

from . import views, api


urlpatterns = [
    path('', views.SearchView.as_view(), name='search'),
    # API views
    path('api/', api.SearchPublicNotesView.as_view(), name='api_search_public_notes')
]
