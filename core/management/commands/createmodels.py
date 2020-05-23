from django.core.management.base import BaseCommand, CommandError

from notes.models import Note, NoteMetaData
from users.models import User, UserPreferences


class Command(BaseCommand):
    help = 'Creat db models in database.'

    def handle(self, *args, **options):     
        for note in Note.objects.all():
            NoteMetaData.objects.create(note=note)

        for user in User.objects.all():
            UserPreferences.objects.create(user=user)
            
        self.stdout.write(self.style.SUCCESS('Successful'))

        