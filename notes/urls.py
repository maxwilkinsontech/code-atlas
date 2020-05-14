from django.urls import path

from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.CreateNote.as_view(), name='create_note'),
    path('view/<pk>/', views.ViewNote.as_view(), name='view_note'),
    path('edit/<pk>/', views.EditNote.as_view(), name='edit_note'),
]
