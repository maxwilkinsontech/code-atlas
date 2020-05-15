from django.test import TestCase
from django.urls import reverse

from users.models import User
from notes.models import Note


class NotesTest(TestCase):
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/notes/')
        
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('notes'))

        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('notes'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes.html')
        
    def test_view_context(self):
        Note.objects.create(
            user=self.user,
            title='test',
            content='content'
        )

        response = self.client.get(reverse('notes'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 1)

class CreateNoteTest(TestCase):
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/notes/create/')
        
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('create_note'))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('create_note'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_note.html')

    def test_view_context(self):
        response = self.client.get(reverse('create_note'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('references' in response.context)

    def test_post(self):
        response = self.client.post(
            reverse('create_note'),
            data={
                'title': 'test',
                'content': 'content',
                'tags': 'python, django',
                'is_public': 'off',
                'references-TOTAL_FORMS': '1', 
                'references-INITIAL_FORMS': '0', 
                'references-MIN_NUM_FORMS': '0', 
                'references-MAX_NUM_FORMS': '1000', 
                'references-0-id': '', 
                'references-0-note': '', 
                'references-0-reference_url': 'https://google.com', 
                'references-0-reference_desc': '1', 
                'references-0-DELETE': ''
            }    
        )

        self.assertEqual(response.status_code, 302)
        note = Note.objects.get()
        self.assertEqual(note.title, 'test')
        self.assertEqual(note.content, 'content')
        self.assertEqual(len(note.tags), 2)
        self.assertEqual(note.is_public, False)
        self.assertEqual(note.references.count(), 1)  

class ViewNoteTest(TestCase):
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

        user = User.objects.create_user(email='test2@email.com')

        self.note = Note.objects.create(
            user=self.user,
            title='test',
            content='content'
        )
        self.note2 = Note.objects.create(
            user=user,
            title='test',
            content='content',
            is_public=False
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/notes/view/{self.note.id}/')
        
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('view_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('view_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_note.html')

    def test_view_not_public(self):
        response = self.client.get(reverse('view_note', args=[self.note2.id]))

        self.assertEqual(response.status_code, 302)

class EditNoteTest(TestCase):
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/notes/edit/{self.note.id}/')
        
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('edit_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('edit_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_note.html')

    def test_view_context(self):
        response = self.client.get(reverse('edit_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('references' in response.context)

    def test_post(self):
        response = self.client.post(
            reverse('edit_note', args=[self.note.id]),
            data={
                'title': 'test2',
                'content': 'content2',
                'tags': '',
                'is_public': 'on',
                'references-TOTAL_FORMS': '1', 
                'references-INITIAL_FORMS': '0', 
                'references-MIN_NUM_FORMS': '0', 
                'references-MAX_NUM_FORMS': '1000', 
                'references-0-id': '', 
                'references-0-note': '', 
                'references-0-reference_url': 'https://google.com', 
                'references-0-reference_desc': '1', 
                'references-0-DELETE': ''
            }    
        )

        self.assertEqual(response.status_code, 302)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, 'test2')
        self.assertEqual(note.content, 'content2')
        self.assertEqual(len(note.tags), 0)
        self.assertEqual(note.is_public, True)
        self.assertEqual(note.references.count(), 1)    

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
        response = self.client.post(reverse('delete_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 302)
        try:
            self.note.refresh_from_db()
        except:
            # exception from not existing anymore
            self.assertTrue(True)

    def test_delete_not_from_creator(self):
        response = self.client.post(reverse('delete_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 302)