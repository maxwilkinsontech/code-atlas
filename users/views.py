from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.views.generic import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import SignUpForm, SettingsForm


class SignUp(FormView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('notes')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super(SignUp, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)

class Settings(LoginRequiredMixin, FormView):
    template_name = 'settings.html'
    success_url = '/accounts/settings/'

    def get_form(self, form_class=None):
        return SettingsForm(self.request.user)