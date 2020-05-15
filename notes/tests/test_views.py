from django.test import TestCase
from django.urls import reverse

from users.models import User
from notes.models import Note

class DeleteNoteTest(TestCase):
    def setUp(self):
        # Login User
        self.user = User.objects.create_user(email='test@email.com')
        psw = 'password'
        self.user.set_password(psw)
        self.user.save()
        self.client.login(
            email=self.user.email,
            password=psw
        )
        self.note = Note.objects.create(
            user=self.user,
            title='test',
            content='content'
        )

    def test_delete_from_creator(self):
        response = self.client.post(reverse('account_settings'))

        self.assertEqual(response.status_code, 302)

    def test_delete_not_from_creator(self):
        response = self.client.post(reverse('account_settings'))

        self.assertEqual(response.status_code, 302)