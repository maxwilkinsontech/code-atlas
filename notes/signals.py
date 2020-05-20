from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Note, NoteMetaData


@receiver(post_save, sender=Note)
def create_note_meta_data(sender, instance, created, **kwargs):
    """
    Create a NoteMetaData for a newly created Note model.
    """
    if created:
        NoteMetaData.objects.create(note=instance)