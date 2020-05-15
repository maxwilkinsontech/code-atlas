from django.forms import ModelForm, inlineformset_factory

from .models import Note, Reference


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Keep the title short but descriptive',
        })
        self.fields['content'].widget.attrs.update({
            'placeholder': 'To include code with highlighting: \n\n```python\ndef some_function():\n\treturn 1\n\nsome_function()\n```',
        })

class ReferenceForm(ModelForm):
    class Meta:
        model = Reference
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ReferenceForm, self).__init__(*args, **kwargs)
        self.fields['reference_url'].widget.attrs.update({
            'placeholder': 'Reference URL',
        })
        self.fields['reference_desc'].widget.attrs.update({
            'placeholder': 'Notes about reference',
            'rows': 1
        })

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