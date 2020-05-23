from django.core.management.base import BaseCommand, CommandError

from notes.models import Note, NoteMetaData
from users.models import User, UserPreferences


class Command(BaseCommand):
    help = 'Migrate the database to the `new` database format.'

    def handle(self, *args, **options):     
        for user in User.objects.all():
            user.save()
        self.stdout.write(self.style.SUCCESS('Successful'))

        