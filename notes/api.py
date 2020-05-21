from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

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
    def post(self, request):
        notes = self.get_queryset()
        notes.update(is_public=True)
        return Response(status=status.HTTP_200_OK)

class NotesMakePrivateView(MutlipleNoteIdsMixin):
    """
    Make the Notes with ids passed private.
    """
    def post(self, request):
        notes = self.get_queryset()
        notes.update(is_public=False)
        return Response(status=status.HTTP_200_OK)

class NotesAddTagsView(MutlipleNoteIdsMixin):
    """
    Add tags to the Notes with ids passed.
    """
    def post(self, request):
        notes = self.get_queryset()
        # notes.delete()
        return Response(status=status.HTTP_200_OK)

class NotesDeleteView(MutlipleNoteIdsMixin):
    """
    Delete Notes with ids passed.
    """
    def post(self, request):
        notes = self.get_queryset()
        notes.delete()
        return Response(status=status.HTTP_200_OK)
