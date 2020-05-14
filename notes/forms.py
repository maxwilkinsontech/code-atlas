from django.forms import ModelForm, inlineformset_factory

from .models import Note, Reference


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body']

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['title'].help_text = 'Keep the title short but descriptive. You\'ll use this title to find this note in the future.'
        self.fields['body'].help_text = 'Write you note content. You can use markdown for better formatting.'

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