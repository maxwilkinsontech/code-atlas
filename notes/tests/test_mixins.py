from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse

from notes.mixins import NoteCreatorMixin, NoteCreatorOrPublicMixin, NoteFormMixin
from notes.models import Note
from users.models import User


factory = RequestFactory()

class NoteCreatorMixinTest(TestCase):

    class TestMixin(NoteCreatorMixin):
        def get_object(self):
           return Note.objects.get()

    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()

        self.note = Note.objects.create(
            user=self.user,
            title='test',
            content='content'
        )

        self.mixin = self.TestMixin()

    def test_user_not_authenticated(self):
        request = factory.get(reverse('home'))
        request.user = AnonymousUser()
        dispatch = self.mixin.dispatch(request)

        self.assertEqual(dispatch.status_code, 302)

    def test_user_not_owner(self):
        request = factory.get(reverse('home'))
        request.user = User.objects.create_user(email='test2@email.com')
        dispatch = self.mixin.dispatch(request)

        self.assertEqual(dispatch.status_code, 302)

class NoteCreatorOrPublicMixinTest(TestCase):

    class TestMixin(NoteCreatorOrPublicMixin):
        def get_object(self):
           return Note.objects.get()

    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()

        self.note = Note.objects.create(
            user=self.user,
            title='test',
            content='content',
            is_public=False
        )

        self.mixin = self.TestMixin()

    def test_user_not_authenticated(self):
        request = factory.get(reverse('home'))
        request.user = AnonymousUser()
        dispatch = self.mixin.dispatch(request)

        self.assertEqual(dispatch.status_code, 302)

    def test_user_not_owner_and_not_public(self):
        request = factory.get(reverse('home'))
        request.user = User.objects.create_user(email='test2@email.com')
        dispatch = self.mixin.dispatch(request)

        self.assertEqual(dispatch.status_code, 302)

class NoteFormMixinTest(TestCase):

    class HelperClass:
        def get_context_data(self, **kwargs):
            return {
                'title': 'test', 
                'content': 'content', 
                'tags': 'python', 
                'is_public': 'on', 
                'references-TOTAL_FORMS': '1', 
                'references-INITIAL_FORMS': '0', 
                'references-MIN_NUM_FORMS': '0', 
                'references-MAX_NUM_FORMS': '1000', 
                'references-0-id': '', 
                'references-0-note': '', 
                'references-0-reference_url': 'https://google.com', 
                'references-0-reference_desc': 'ref', 
                'references-0-DELETE': ''
            }

    class TestMixin(NoteFormMixin, HelperClass):
        pass

    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()

        self.note = Note.objects.create(
            user=self.user,
            title='test',
            content='content',
        )

        self.mixin = self.TestMixin()
        self.mixin.object = self.note

    def test_get_context_data_has_references_get(self):
        request = factory.get(reverse('home'))
        self.mixin.request = request
        data = self.mixin.get_context_data()

        self.assertTrue('references' in data)

    def test_get_context_data_has_references_post(self):
        request = factory.post(reverse('home'))
        self.mixin.request = request
        data = self.mixin.get_context_data()

        self.assertTrue('references' in data)

    def test_success_url(self):
        url = self.mixin.success_url()

        self.assertEqual(url, f'/notes/view/{self.note.id}/')