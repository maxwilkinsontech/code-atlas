import csv

from django.core.management.base import BaseCommand, CommandError

from notes.models import Note
from users.models import User


class Command(BaseCommand):
    help = 'Populate the Note table with mock data'

    def handle(self, *args, **options):
        user = User.objects.get(email='admin@admin.com')
        with open('static/data/note_mock_data.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                Note.objects.create(
                    user=user,
                    title=row[0],
                    content=row[1]
                )
                
            self.stdout.write(self.style.SUCCESS('Successfully loaded data'))