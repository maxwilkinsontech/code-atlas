from django.db import models

from core.models import DateModel
from users.models import User


class Note(DateModel):
    """
    Model to represent a memorable point.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    is_private = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    body = models.TextField()

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


