from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase

from notes.models import Note
from users.models import User


class NotesMakePublicViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

        self.note = Note.objects.create(
            user=self.user,
            title='test',
            content='content',
            is_public=False
        )
        self.note2 = Note.objects.create(
            user=self.user,
            title='test',
            content='content',
            is_public=False
        )
        
        self.data = {
            'ids[]': [self.note.id]
        }
        self.data2 = {
            'ids[]': [self.note.id, self.note2.id]
        }

    def test_post_no_data(self):
        response = self.client.post(
            '/notes/api/public/',
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(self.note.is_public)

    def test_post_single_id(self):
        response = self.client.post(
            '/notes/api/public/',
            data=self.data,
            format='json'
        )
        self.note.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.note.is_public)

    def test_post_multiple_ids(self):
        response = self.client.post(
            '/notes/api/public/',
            data=self.data2,
            format='json'
        )
        self.note.refresh_from_db()
        self.note2.refresh_from_db()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.note.is_public)
        self.assertTrue(self.note2.is_public)

class NotesMakePrivateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

        self.note = Note.objects.create(
            user=self.user,
            title='test',
            content='content',
            is_public=True
        )
        self.note2 = Note.objects.create(
            user=self.user,
            title='test',
            content='content',
            is_public=True
        )
        
        self.data = {
            'ids[]': [self.note.id]
        }
        self.data2 = {
            'ids[]': [self.note.id, self.note2.id]
        }

    def test_post_no_data(self):
        response = self.client.post(
            '/notes/api/private/',
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(self.note.is_public)

    def test_post_single_id(self):
        response = self.client.post(
            '/notes/api/private/',
            data=self.data,
            format='json'
        )
        self.note.refresh_from_db()
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.note.is_public)

    def test_post_multiple_ids(self):
        response = self.client.post(
            '/notes/api/private/',
            data=self.data2,
            format='json'
        )
        self.note.refresh_from_db()
        self.note2.refresh_from_db()
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.note.is_public)
        self.assertFalse(self.note2.is_public)

class NotesAddTagsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

        self.note = Note.objects.create(
            user=self.user,
            title='test',
            content='content',
        )
        self.note2 = Note.objects.create(
            user=self.user,
            title='test',
            content='content',
        )
        self.note2.tags = 'initial'

        self.data = {
            'ids[]': [self.note.id],
            'tags': 'test'
        }
        self.data2 = {
            'ids[]': [self.note.id, self.note2.id],
            'tags': 'test, django'
        }

    def test_post_no_data(self):
        response = self.client.post(
            '/notes/api/tags/',
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.note.tags_to_string(), '')

    def test_post_single_id(self):
        response = self.client.post(
            '/notes/api/tags/',
            data=self.data,
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.note.tags_to_string(), 'test')

    def test_post_multiple_ids(self):
        response = self.client.post(
            '/notes/api/tags/',
            data=self.data2,
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.note.tags_to_string(), 'django, test')
        self.assertEqual(self.note2.tags_to_string(), 'django, initial, test')

class NotesDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

        self.note = Note.objects.create(
            user=self.user,
            title='test',
            content='content',
        )
        self.note2 = Note.objects.create(
            user=self.user,
            title='test2',
            content='content',
        )

        self.data = {
            'ids[]': [self.note.id]
        }
        self.data2 = {
            'ids[]': [self.note.id, self.note2.id]
        }

    def test_post_no_data(self):
        response = self.client.post(
            '/notes/api/delete/',
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(self.note)
        self.assertIsNotNone(self.note2)

    def test_post_single_id(self):
        response = self.client.post(
            '/notes/api/delete/',
            data=self.data,
            format='json'
        )

        note = Note.objects.filter(title='test')
        note2 = Note.objects.filter(title='test2')
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(note.exists())
        self.assertTrue(note2.exists())

    def test_post_multiple_ids(self):
        response = self.client.post(
            '/notes/api/delete/',
            data=self.data2,
            format='json'
        )

        note = Note.objects.filter(title='test')
        note2 = Note.objects.filter(title='test2')

        self.assertEqual(response.status_code, 204)
        self.assertFalse(note.exists())
        self.assertFalse(note2.exists())