from django.forms import ModelForm, inlineformset_factory

from .models import Note, Reference


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body']


class ReferenceForm(ModelForm):
    class Meta:
        model = Reference
        exclude = ()

ReferenceFormSet = inlineformset_factory(
    Note,
    Reference,
    form=ReferenceForm,
    fields=[
        'reference_url',
        'reference_desc'
    ],
    extra=1,
    can_delete=True
)