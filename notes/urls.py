from django.urls import path

from . import views


urlpatterns = [
    path('', views.NotesView.as_view(), name='notes'),
    path('create/', views.CreateNoteView.as_view(), name='create_note'),
    path('view/<pk>/', views.ViewNoteView.as_view(), name='view_note'),
    path('edit/<pk>/', views.EditNoteView.as_view(), name='edit_note'),
    path('delete/<pk>/', views.DeleteNoteView.as_view(), name='delete_note'),
]