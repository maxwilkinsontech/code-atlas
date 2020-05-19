from django.test import TestCase

from notes.models import Note, NoteMetaData
from users.models import User


class CreateCoteMetaDataSignalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@email.com')

    def test_meta_create_when_note_created(self):
        meta_count = NoteMetaData.objects.count()
        Note.objects.create(user=self.user, title='a', content='b')
        self.assertEqual(meta_count + 1, NoteMetaData.objects.count())
           
    def test_meta_not_create_when_note_saved(self):
        note = Note.objects.create(user=self.user, title='a', content='b')
        meta_count = NoteMetaData.objects.count()
        note.save()
        self.assertEqual(meta_count, NoteMetaData.objects.count())