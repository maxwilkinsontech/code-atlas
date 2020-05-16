from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path('settings/', 
        views.Settings.as_view(), 
        name='account_settings'
    ),
    path('settings/delete-account/', 
        views.DeleteAccount.as_view(), 
        name='delete_account'
    ),
    path('signup/', 
        views.SignUp.as_view(), 
        name='signup'
    ),
    path('signin/', 
        auth_views.LoginView.as_view(
            template_name='signin.html',
            redirect_authenticated_user=True
        ), 
        name='login'
    ),
    path('logout/', 
        auth_views.LogoutView.as_view(), 
        name='logout'
    ),
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='password_reset/password_reset.html',
            html_email_template_name='password_reset/password_reset_html_email.html'
        ), 
        name='password_reset'
    ),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset/password_reset_done.html'
        ), 
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset/reset.html', 
            success_url=reverse_lazy('password_reset_complete')
        ), 
        name='password_reset_confirm'
    ),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset/reset_done.html'
        ), 
        name='password_reset_complete'
    ),
]
