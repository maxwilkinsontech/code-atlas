from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import AppConfig


class NotesConfig(AppConfig):
    name = 'notes'

    def ready(self):
        from . import signals