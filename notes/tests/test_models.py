from django.test import TestCase

from notes.models import Note
from users.models import User


class NoteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.note = Note.objects.create(
            user=self.user,
            title='test',
            content='content'
        )
        self.note2 = Note.objects.create(
            user=self.user,
            title='test',
            content='content'
        )

    def test_tags_to_string(self):
        test_tags = self.note.tags_to_string()
        expected_tags = ', '.join([str(i) for i in self.note.tags])

        self.assertEqual(test_tags, expected_tags)

    def test_increment_clone_count(self):
        clones_before = self.note.meta_data.num_clones
        self.note.increment_clone_count(self.note2)
        self.note.meta_data.refresh_from_db()
        clones_after = self.note.meta_data.num_clones

        self.assertEqual(clones_before + 1, clones_after)

    def test_increment_clone_count_cloned_note_field(self):
        self.note.increment_clone_count(self.note2)
        self.note2.meta_data.refresh_from_db()

        self.assertIsNotNone(self.note2.meta_data.cloned_note)

    def test_increment_view_count(self):
        views_before = self.note.meta_data.num_views
        self.note.increment_view_count()
        self.note.meta_data.refresh_from_db()
        views_after = self.note.meta_data.num_views

        self.assertEqual(views_before + 1, views_after)