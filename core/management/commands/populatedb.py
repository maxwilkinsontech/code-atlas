import random
import csv
import string

from django.core.management.base import BaseCommand, CommandError

from essential_generators import DocumentGenerator

from notes.models import Note
from users.models import User


class Command(BaseCommand):
    help = 'Populate the Note table with mock data'

    def handle(self, *args, **options):     
        gen = DocumentGenerator()      
        user_count = 1
        index = 1
        num_notes = None
        user = None

        while True:
            if index == 1:
                user = User.objects.create_user(email=f'{user_count}@email.com')
                num_notes = random.randint(20, 100)
            elif index > num_notes:
                index = 1
                user_count += 1
                print(f'Created Notes for User [{user_count}/10000]', end='\r')
                continue

            note = Note.objects.create(
                user=user,
                title=gen.sentence(),
                content=gen.paragraph()
            )
            note.tags = gen.word()

            index += 1

        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))

        