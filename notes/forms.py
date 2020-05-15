from django import forms

from .models import Note, Reference


class NoteForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='Adding tags will make filtering and finding Notes easier.'
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'tags']

    def __init__(self, note=None, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'placeholder': 'Keep the title short but descriptive',
        })
        self.fields['content'].widget.attrs.update({
            'placeholder': 'To include code with highlighting: \n\n```python\ndef some_function():\n\tpass\n\nsome_function()\n```',
        })
        self.fields['tags'].widget.attrs.update({
            'placeholder': 'Provide a comma seperated list of tags e.g. python, django',
        })
        if note:
            self.fields['tags'].initial = ', '.join([str(i) for i in note.tags])

class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ReferenceForm, self).__init__(*args, **kwargs)
        self.fields['reference_url'].widget.attrs.update({
            'placeholder': 'Reference URL',
        })
        self.fields['reference_desc'].widget.attrs.update({
            'placeholder': 'Reference notes',
            'rows': 1
        })

ReferenceFormSet = forms.inlineformset_factory(
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