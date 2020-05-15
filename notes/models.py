from django.db import models

from core.models import DateModel
from users.models import User


class Note(DateModel):
    """
    Model to represent a memorable point.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='notes'
    )
    title = models.CharField(
        max_length=255,
        help_text='You\'ll use the title to find this note in the future.'
    )
    content = models.TextField(
        help_text='Write your note content here. You can use markdown for better formatting.'
    )
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.title

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


