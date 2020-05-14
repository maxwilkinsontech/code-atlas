from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class SettingsForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.email

    def save(self):
        cd = self.cleaned_data
        first_name = cd.get('first_name')
        last_name = cd.get('last_name')
        email = cd.get('email')
        password = cd.get('password')
        user = self.user

        print(first_name)

        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None and email != '':
            user.email = email
        if password is not None and password != '':
            user.set_password(password)
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        user.save()
        return user
        