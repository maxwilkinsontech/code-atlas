import random
import string 

from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.db import models

from tagging.registry import register

from core.models import DateModel
from users.models import User


class Note(DateModel):
    """
    Model to represent a memorable point.
    `document_vector` is an indexed field with the value of the concatenation of `title` and 
    `content`. The field is updated whenever the save method is called.
    """
    id = models.IntegerField(primary_key=True, blank=True, unique=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='notes'
    )
    title = models.CharField(
        max_length=255,
        help_text='You\'ll use the title to find this Note in the future.'
    )
    content = models.TextField(
        help_text='Write your Note content here. You can use markdown for better formatting.'
    )
    is_public = models.BooleanField(default=True)
    # Indexed columns for searching.
    document_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [GinIndex(fields=['document_vector',])]

    def save(self, *args, **kwargs):
        """Generate a random id of length 10 of numerical characters"""
        if not self.id:
            while True:
                id = ''.join(random.choice(string.digits) for _ in range(8))
                if not Note.objects.filter(id=id).exists():
                    break
            self.id = id
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def tags_to_string(self):
        """
        Return the Note's tags a comma seperated string.
        """
        tags = ', '.join([str(i) for i in self.tags])
        return tags

    def increment_clone_count(self):
        """
        Increment the clone count for the given Note.
        """
        meta_data = self.meta_data
        meta_data.num_clones += 1
        meta_data.save()

    def increment_view_count(self):
        """
        Increment the view count for the given Note.
        """
        meta_data = self.meta_data
        meta_data.num_views += 1
        meta_data.save()

class Reference(DateModel):
    """
    Model to store a reference link. Associated to a Note.
    """
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='references'
    )
    reference_url = models.URLField()
    reference_desc = models.TextField(
        max_length=255, 
        blank=True
    )

    def __str__(self):
        return self.reference_url

class NoteMetaData(models.Model):
    """
    Model to store meta data for a Note. `note` is the created Note and `cloned_note` is the Note 
    in which the new Note is cloned from.
    """
    note = models.OneToOneField(
        Note,
        on_delete=models.CASCADE,
        related_name='meta_data'
    )
    cloned_note = models.ForeignKey(
        Note,
        on_delete=models.SET_NULL,
        related_name='clones',
        null=True
    )
    num_views = models.PositiveIntegerField(default=0)
    num_clones = models.PositiveIntegerField(default=0)

# Register Note model for tagging
register(Note)
