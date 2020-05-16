from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class SettingsForm(forms.Form):
    email = forms.EmailField(
        required=False,
        help_text='Do not change your email if you used a third party login. Set a password first.')
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

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '')
        
        # Make sure email is not already in use.
        if email != '' and email != self.user.email:
            existing_user = User.objects.filter(email=email)
            if existing_user.exists():
                self.add_error('email', 'User with this Email address already exists.')

    def save(self):
        user = self.user
        cd = self.cleaned_data
        email = cd.get('email', '')
        password = cd.get('password', '')

        if email != '':
            user.email = email
            
        if password != '':
            user.set_password(password)
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        user.save()
        return user
        