var simplemde = new SimpleMDE({
    status: false,
    spellChecker: false,
    renderingConfig: {
        codeSyntaxHighlighting: true,
    },
    showIcons: ['code', 'table', 'redo', 'heading', 'undo', 'strikethrough'],
    hideIcons: ['side-by-side', 'fullscreen'],
});

$('.formset_row').formset({
    addText: 'Add another reference +',
    deleteText: 'X',
    prefix: 'references'
});