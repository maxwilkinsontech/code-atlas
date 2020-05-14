from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.db import transaction

from .models import Note
from .forms import NoteForm, ReferenceFormSet


class Notes(LoginRequiredMixin, ListView):
    """
    List a User's Notes.
    """
    template_name = 'notes.html'
    model = Note

class CreateNote(LoginRequiredMixin, CreateView):
    """
    View for User to create a new Note.
    """
    template_name = 'create_note.html'
    model = Note
    fields = ['title', 'body']

    def success_url(self):
        return reverse_lazy('view_note', args=[self.object.id])

    def get_context_data(self, **kwargs):
        data = super(CreateNote, self).get_context_data(**kwargs)
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
            self.object = form.save()
            if references.is_valid():
                references.instance = self.object
                references.save()
        return redirect(self.success_url())

class ViewNote(DetailView):
    """
    View for a user to view a Note.
    """ 
    template_name = 'view_note.html'
    model = Note

class EditNote(LoginRequiredMixin, DetailView):
    pass