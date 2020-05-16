from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .mixins import NoteFormMixin, NoteCreatorMixin, NoteCreatorOrPublicMixin
from .models import Note
from .forms import NoteForm


class NotesView(LoginRequiredMixin, ListView):
    """
    List a User's Notes ordered by most recently edited. Results split into pages of 24 objects.
    """
    template_name = 'notes.html'
    paginate_by = 24
    model = Note

    def get_queryset(self):
        return self.request.user.notes.order_by('-last_edited')

class CreateNoteView(LoginRequiredMixin, NoteFormMixin, CreateView):
    """
    View for User to create a new Note.
    """
    template_name = 'create_note.html'
    model = Note
    form_class = NoteForm

class ViewNoteView(NoteCreatorOrPublicMixin, DetailView):
    """
    View for a user to view a Note. If the not is not public, only the owner can view it.
    """ 
    template_name = 'view_note.html'
    model = Note

class EditNoteView(NoteCreatorMixin, NoteFormMixin, UpdateView):
    """
    View to edit a note. Only the owner of a Note can edit it.
    """
    template_name = 'edit_note.html'
    model = Note
    form_class = NoteForm

class DeleteNoteView(NoteCreatorMixin, DeleteView):
    """
    View to delete a note. Only the owner of a Note can delete it.
    """
    model = Note
    success_url = reverse_lazy('notes')