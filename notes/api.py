from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import status

from tagging.models import Tag

from .mixins import MutlipleNoteIdsMixin
from .serializers import NoteSerializer


class NotesListView(ListAPIView):
    """
    Returns list of Notes.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return self.request.user.notes.all()

class NotesMakePublicView(MutlipleNoteIdsMixin):
    """
    Make the Notes with ids passed public.
    """
    def perform_action(self, notes):
        notes.update(is_public=True)        

class NotesMakePrivateView(MutlipleNoteIdsMixin):
    """
    Make the Notes with ids passed private.
    """
    def perform_action(self, notes):
        notes.update(is_public=False)

class NotesAddTagsView(MutlipleNoteIdsMixin):
    """
    Add tags to the Notes with ids passed.
    """
    def perform_action(self, notes):
        tags = self.request.data.get('tags', '')
        tags_list = tags.split(', ')
        if tags:
            for note in notes:
                for tag in tags_list:
                    Tag.objects.add_tag(note, tag)

class NotesDeleteView(MutlipleNoteIdsMixin):
    """
    Delete Notes with ids passed.
    """
    success_status = status.HTTP_204_NO_CONTENT

    def perform_action(self, notes):
        notes.delete()
