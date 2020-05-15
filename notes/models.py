import random
import string 

from django.db import models

from tagging.registry import register

from core.models import DateModel
from users.models import User


class Note(DateModel):
    """
    Model to represent a memorable point.
    """
    id = models.IntegerField(
        primary_key=True, 
        blank=True, 
        unique=True
    )
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

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Generate a random id of length 10 of numerical characters"""
        if not self.id:
            while True:
                id = ''.join(random.choice(string.digits) for _ in range(8))
                if not Note.objects.filter(id=id).exists():
                    break
            self.id = id
        super(Note, self).save(*args, **kwargs)

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
    reference_desc = models.TextField(max_length=255, blank=True)

# Register Note model for tagging
register(Note)
