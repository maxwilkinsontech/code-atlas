from django.contrib import admin

from .models import Note, Reference


class ReferenceInLine(admin.TabularInline):
    model = Reference
    extra = 0

class NoteAdmin(admin.ModelAdmin):
    model = Note
    inlines = [ReferenceInLine]

admin.site.register(Note, NoteAdmin)