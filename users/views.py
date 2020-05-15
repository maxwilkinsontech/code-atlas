from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.views.generic import FormView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import SignUpForm, SettingsForm
from .models import User


class SignUp(FormView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('dashboard')

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
    form_class = SettingsForm
    
    def get_form_kwargs(self):
        kwargs = super(Settings, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class DeleteAccount(LoginRequiredMixin, DeleteView):
    """
    Delete a User account and all data associated with it.
    """
    model = User
    slug_field = 'email'
    success_url = reverse_lazy('home')