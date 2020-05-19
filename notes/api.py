from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from notes.serializers import NoteSerializer


class NoteListView(ListAPIView):
    """
    Returns list of Notes.
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notes.all()
