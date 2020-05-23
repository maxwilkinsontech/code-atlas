from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']

class SettingsForm(forms.Form):
    username = forms.CharField(
        help_text='This will be displayed on your public profile'
    )
    email = forms.EmailField(
        help_text='Do not change your email without setting a password first.')
    password = forms.CharField(
        required=False, 
        widget=forms.PasswordInput,
        help_text='Enter a new password.'
    )

    def __init__(self, request, user, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.request = request
        self.user = user
        self.fields['email'].initial = user.email
        self.fields['username'].initial = user.username

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '')
        username = cleaned_data.get('username', '')
        
        # Make sure email is not already in use.
        if email != '' and email != self.user.email:
            existing_user = User.objects.filter(email=email)
            if existing_user.exists():
                self.add_error('email', 'User with this Email address already exists.')
        # Make sure username is not already in use.
        if username != '' and username != self.user.username:
            existing_profile = User.objects.filter(username=username)
            if existing_profile.exists():
                self.add_error('username', 'This username is already taken.')
        

    def save(self):
        user = self.user
        cd = self.cleaned_data
        username = cd.get('username', '')
        email = cd.get('email', '')
        password = cd.get('password', '')

        if username != '':
            user.username = username

        if email != '':
            user.email = email
            
        if password != '':
            user.set_password(password)
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        user.save()
        return user
        