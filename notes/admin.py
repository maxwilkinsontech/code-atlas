from django.contrib import admin

from .models import Note, Reference, NoteMetaData

class NoteMetaDataInLine(admin.TabularInline):
    model = NoteMetaData
    extra = 0

class ReferenceInLine(admin.TabularInline):
    model = Reference
    extra = 0

class NoteAdmin(admin.ModelAdmin):
    model = Note
    inlines = [ReferenceInLine, NoteMetaDataInLine]

admin.site.register(Note, NoteAdmin)