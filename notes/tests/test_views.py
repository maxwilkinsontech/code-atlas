from django.test import TestCase
from django.urls import reverse

from notes.models import Note, Reference
from users.models import User


class NotesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

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

class NotesTagsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')
        
        self.note = Note.objects.create(
            user=self.user,
            title='test',
            content='content'
        )
        self.note.tags = 'test1, test2, test three'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/notes/mode/tags/')
        
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('notes_mode_tags'))

        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('notes_mode_tags'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes_tags.html')

    def test_get_queryset_correct(self):
        response = self.client.get(reverse('notes_mode_tags'))

        self.assertEqual(response.status_code, 200)
        tags_string = [x.name for x in response.context['object_list']]
        self.assertEqual(tags_string, ['test2', 'test1', 'test three'])

class CreateNoteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

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

    def test_view_correct_context(self):
        response = self.client.get(reverse('create_note'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('references' in response.context)

    def test_view_create_note_on_post(self):
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
            }    
        )

        self.assertEqual(response.status_code, 302)
        note = Note.objects.get()
        self.assertEqual(note.title, 'test')
        self.assertEqual(note.content, 'content')
        self.assertEqual(len(note.tags), 2)
        self.assertEqual(note.is_public, False)
        self.assertEqual(note.references.count(), 1)  

class ViewNoteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

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

class EditNoteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')

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

    def test_view_correct_context(self):
        response = self.client.get(reverse('edit_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('references' in response.context)

    def test_view_update_note_on_post(self):
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
            }    
        )

        self.assertEqual(response.status_code, 302)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, 'test2')
        self.assertEqual(note.content, 'content2')
        self.assertEqual(len(note.tags), 0)
        self.assertEqual(note.is_public, True)
        self.assertEqual(note.references.count(), 1)    

class DeleteNoteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')
        
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
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_delete_not_from_creator(self):
        response = self.client.post(reverse('delete_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(self.note)

class CloneNoteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@email.com')
        self.user.set_password('password')
        self.user.save()
        self.client.login(email=self.user.email, password='password')
        
        self.note = Note.objects.create(
            user=self.user,
            title='test',
            content='content'
        )
        self.note.tags = 'test'
        Reference.objects.create(
            note=self.note,
            reference_url='https://google.com/'
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/notes/create/clone/{self.note.id}/')
        
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('clone_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('clone_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clone_note.html')

    def test_dispatch_note_not_public(self):
        user = User.objects.create_user(email='test2@email.com')
        note = Note.objects.create(
            user=user,
            title='test',
            content='content',
            is_public=False
        )
        response = self.client.get(reverse('clone_note', args=[note.id]))

        self.assertEqual(response.status_code, 302)

    def test_dispatch_note_public(self):
        user = User.objects.create_user(email='test2@email.com')
        note = Note.objects.create(
            user=user,
            title='test',
            content='content',
        )
        response = self.client.get(reverse('clone_note', args=[note.id]))

        self.assertEqual(response.status_code, 200)

    def test_dispatch_note_not_public_but_note_creator(self):
        self.note.is_public = False
        self.note.save()
        response = self.client.get(reverse('clone_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 200)

    def test_get_initial_correct(self):
        response = self.client.get(reverse('clone_note', args=[self.note.id]))

        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIsNotNone(form['title'], self.note.title)
        self.assertIsNotNone(form['content'], self.note.content)
        self.assertIsNotNone(form['tags'], 'test')
        self.assertEqual(len(response.context['references']), 1)

    def test_post_clone_incremented(self):
        clones_before = self.note.meta_data.num_clones
        response = self.client.post(
            reverse('clone_note', args=[self.note.id]),
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
            }     
        )

        self.note.meta_data.refresh_from_db()
        clones_after = self.note.meta_data.num_clones

        self.assertEqual(response.status_code, 302)
        self.assertEqual(clones_before + 1, clones_after)