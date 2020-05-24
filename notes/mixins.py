from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db import transaction

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .forms import ReferenceFormSet
from .models import NoteMetaData


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
        if note.user != user:
            return redirect('view_note', note.id)
        return super().dispatch(request, *args, **kwargs)

class NoteCreatorOrPublicMixin(AccessMixin):
    """
    Mixin to prevent a User other than the owner from viewing non-public Note.
    """
    is_note_owner = True

    def dispatch(self, request, *args, **kwargs):
        note = self.get_object()
        user = request.user
        # Check user is authenticated.
        if not user.is_authenticated:
            return redirect('login')
        # Check user is creator of note or note is public.
        if note.user != user:
            self.is_note_owner = False
            if not note.is_public:
                return redirect('notes')
        # Passed checks, increment view count.
        note.increment_view_count()
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

# --------------------------------------------------------------------------------------------------
#                                   Rest Framework Mixins
# --------------------------------------------------------------------------------------------------
class MutlipleNoteIdsMixin(APIView):
    """
    Mixin to be used a base class by API views that deal with multiple ids at once.
    """
    permission_classes = [IsAuthenticated]
    success_status = status.HTTP_200_OK

    def get_queryset(self):
        """
        Return a queryset of Notes matching the ids given.
        """
        ids = dict(self.request.data).get('ids', [])
        queryset = self.request.user.notes.filter(id__in=ids)
        return queryset

    def post(self, request):
        """
        Given a non-empty queryset, perform the action. `perform_action` defined in child class.
        """
        notes = self.get_queryset()
        if notes.exists():
            self.perform_action(notes)
            return Response(status=self.success_status)
        else:
            return  Response(status=status.HTTP_400_BAD_REQUEST)