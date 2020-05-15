from django.views.generic import TemplateView
from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),
    path('term-of-service/', TemplateView.as_view(template_name='terms_of_service.html'), name='terms_of_service'),
]
