from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class SettingsForm(forms.Form):
    email = forms.EmailField(required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['email'].initial = user.email

    def is_valid(self):
        valid = super(SettingsForm, self).is_valid()
        print(valid)
        if not valid:
            return valid

        return False

        cd = self.cleaned_data()
        email = cd.get('email')

        if email is not None and email != '':
            print(email)
            # self.add_error('password', "Incorrect password entered.")
            return False

        return True

    def save(self):
        user = self.user
        cd = self.cleaned_data
        email = cd.get('email')
        password = cd.get('password')

        if email is not None and email != '':
            user.email = email
        if password is not None and password != '':
            user.set_password(password)
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        user.save()
        return user
        