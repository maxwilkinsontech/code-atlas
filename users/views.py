from django.views.generic import FormView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import SignUpForm, SetUsernameForm, SettingsForm
from .models import User, UserPreferences


class SignUp(FormView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('set_username')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('notes')
        return super(SignUp, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)

class SetUsernameView(LoginRequiredMixin, FormView):
    """
    View for a User to set a username as well as set email preferences.
    """
    template_name = 'set_username.html'
    form_class = SetUsernameForm
    success_url = reverse_lazy('notes')

    def dispatch(self, request, *args, **kwargs):
        if request.user.preferences.email_consent is not None:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SetUsernameView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        email_consent = self.request.POST.get('email_consent', False)
        form.save(email_consent)
        return super().form_valid(form)

class Settings(LoginRequiredMixin, FormView):
    template_name = 'settings.html'
    form_class = SettingsForm
    success_url = reverse_lazy('account_settings')
    
    def get_form_kwargs(self):
        kwargs = super(Settings, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class UpdateUserPreferenceView(LoginRequiredMixin, View):
    """
    Update a User's UserPreferences model.
    """
    def get(self, request):
        return redirect('account_settings')

    def post(self, request):
        preferences = self.request.user.preferences
        email_consent = self.request.POST.get('email_consent', False)
        consent = True if email_consent == 'on' else False
        preferences.email_consent = consent
        preferences.save()
        return redirect('account_settings')

class DeleteAccount(LoginRequiredMixin, DeleteView):
    """
    Delete a User account and all data associated with it.
    """
    model = User
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user