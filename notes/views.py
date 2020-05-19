from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import CreateView
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
    model = Note

    def get_template_names(self):
        """
        Render template depending on the User making request.
        """
        if self.request.user == self.get_object().user:
            return 'view_note.html'
        else:
            return 'view_note_public.html'

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

class CloneNoteView(CreateNoteView):
    """
    View for User to make a clone of another Note.
    """
    template_name = 'clone_note.html'
    model = Note

    def get_object(self):
        """
        Can only clone Note if it is public or the requesting User is the creator of the Note.
        """
        note = super().get_object()

        if note.is_public or note.user == self.request.user:
            self.object = note
            return note

        return

    def get_initial(self):
        """
        Add the cloned Note's data to the form.
        """
        initial = super().get_initial()
        note = self.get_object()

        initial['title'] = note.title
        initial['content'] = note.content
        initial['tags'] = note.tags_to_string()

        return initial