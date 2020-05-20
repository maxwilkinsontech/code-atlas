from django.urls import path

from . import views, api


urlpatterns = [
    path('', views.NotesView.as_view(), name='notes'),
    path('mode/edit/', views.NotesEditView.as_view(), name='notes_mode_edit'),
    path('mode/tags/', views.NotesTagsView.as_view(), name='notes_mode_tags'),
    path('create/', views.CreateNoteView.as_view(), name='create_note'),
    path('create/clone/<pk>/', views.CloneNoteView.as_view(), name='clone_note'),
    path('view/<pk>/', views.ViewNoteView.as_view(), name='view_note'),
    path('edit/<pk>/', views.EditNoteView.as_view(), name='edit_note'),
    path('delete/<pk>/', views.DeleteNoteView.as_view(), name='delete_note'),
    # API views
    path('api/', api.NoteListView.as_view(), name='api_notes'),
]