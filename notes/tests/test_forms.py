from django.test import TestCase

from notes.forms import NoteForm
from users.models import User


class NoteFormTests(TestCase):
    def test_form_save(self):
        user = User.objects.create_user(email='test@email.com')
        form_data = {
            'title': 'title',
            'content': 'content'
        }
        post_data = {
            'is_public': 'off',
            'tags': 'python, django'
        }

        form = NoteForm(data=form_data)
        form.instance.user = user
        note = form.save(post_data)

        self.assertEqual(note.title, 'title')
        self.assertEqual(note.content, 'content')
        self.assertEqual(len(note.tags), 2)
        self.assertEqual(note.is_public, False)