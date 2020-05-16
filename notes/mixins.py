from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db import transaction

from .forms import ReferenceFormSet


class NoteCreatorMixin(AccessMixin):
    """
    Mixin to only allow access to a view if the creator of the Note is the User making the request.
    """
    def dispatch(self, request, *args, **kwargs):
        note = self.get_object()
        user = request.user
        # Check user is authenticated.
        if not user.is_authenticated:
            return redirect('login')
        # Check user is creator of note.
        if note.user != request.user:
            return redirect('view_note', note.id)
        return super().dispatch(request, *args, **kwargs)

class NoteCreatorOrPublicMixin(AccessMixin):
    """
    Mixin to prevent a User other than the owner from viewing non-public Note.
    """
    def dispatch(self, request, *args, **kwargs):
        note = self.get_object()
        user = request.user
        # Check user is authenticated.
        if not user.is_authenticated:
            return redirect('login')
         # Check user is creator of note or note is public.
        if not note.is_public and note.user != request.user:
            return redirect('notes')
        return super().dispatch(request, *args, **kwargs)

class NoteFormMixin(object):
    """
    Mixin used in CreateNoteView and EditNoteView. Provides functionality to save the Note ModelForm 
    as well as any Reference FormSets. Additional saves data left in POST to Note model.
    """
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['references'] = ReferenceFormSet(self.request.POST, instance=self.object)
        else:
            data['references'] = ReferenceFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        references = context['references']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save(self.request.POST)
            if references.is_valid():
                references.instance = self.object
                references.save()
        return redirect(self.success_url())

    def success_url(self):
        return reverse_lazy('view_note', args=[self.object.id])