from django.db import models

from users.models import User


class SearchHistory(models.Model):
    """
    Model to store a search query made by a User.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='search_history'
    )
    query = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True)
