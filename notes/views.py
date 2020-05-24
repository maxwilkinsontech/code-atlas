from django.views.generic import DetailView, ListView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from tagging.models import Tag

from .mixins import NoteFormMixin, NoteCreatorMixin, NoteCreatorOrPublicMixin
from .models import Note, NoteMetaData
from .forms import NoteForm


class NotesView(LoginRequiredMixin, ListView):
    """
    List a User's Notes ordered by most recently edited. Results split into pages of 24 objects.
    """
    template_name = 'notes.html'
    paginate_by = 24

    def get_queryset(self):
        return self.request.user.notes.order_by('-last_edited')

class NotesEditModeView(LoginRequiredMixin, ListView):
    """
    Returns a template for editing Notes in the masses easily. Data via api.
    """
    template_name = 'notes_edit.html'
    paginate_by = 100
    
    def get_queryset(self):
        notes = self.request.user.notes.all()
        default_ordering = ['-last_edited', 'title']
        ordering = self.request.GET.get('ordering')

        if ordering in ['public', 'private']:
            is_public = True if ordering == 'public' else False
            queryset = notes.filter(is_public=is_public).order_by(*default_ordering)
        elif ordering in ['date_created', '-date_created', 'last_edited', 
                          '-last_edited', 'title', '-title']:            
            queryset = notes.order_by(ordering)
        else:
            queryset = notes.order_by(*default_ordering)

        return queryset

class NotesTagModeView(LoginRequiredMixin, ListView):
    """
    List a User's Notes ordered by most recently edited. Results split into pages of 24 objects.
    """
    template_name = 'notes_tags.html'
    paginate_by = 100

    def get_queryset(self):
        tags = Tag.objects.usage_for_model(Note, counts=True, filters=dict(user=self.request.user))
        tags = sorted(tags, key=lambda x: (x.count, x.name), reverse=True)
        return tags

class CreateNoteView(LoginRequiredMixin, NoteFormMixin, CreateView):
    """
    View for User to create a new Note.
    """
    template_name = 'create_note.html'
    model = Note
    form_class = NoteForm

class ViewNoteView(NoteCreatorOrPublicMixin, DetailView):
    """
    View for a user to view a Note. If the not is not public, only the owner can view it. The 
    num_views is incremented when by a User viewing a Note via this view. This is done in the mixin.
    """ 
    model = Note

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('meta_data')

    def get_template_names(self):
        """
        Render template depending on the User making request.
        """
        if self.is_note_owner:
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

    def get_success_url(self):
        if self.request.GET.get('edit_mode', False):
            return reverse_lazy('notes_edit_mode')
        return super().get_success_url()

class CloneNoteView(CreateNoteView):
    """
    View for User to make a clone of another Note. The Note's num_clones is incremented upon a 
    sucessful clone.
    """
    template_name = 'clone_note.html'
    model = Note

    def dispatch(self, request, *args, **kwargs):
        """
        Can only clone Note if it is public or the requesting User is the creator of the Note. 
        """
        note = self.get_object()

        if not note.is_public and note.user != self.request.user:
            return redirect('notes')

        self.object = note
        return super().dispatch(request, *args, **kwargs)

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

    def form_valid(self, form):
        """
        Log that the Note has been cloned.
        """
        redirect = super().form_valid(form)
        # Save meta data.
        cloned_note = self.get_object()
        cloned_note.increment_clone_count(self.object)
        return redirect