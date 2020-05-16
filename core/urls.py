from django.views.generic import TemplateView
from django.urls import path


urlpatterns = [
    path(
        '', 
        TemplateView.as_view(template_name='index.html'), 
        name='home'
    ),
    path(
        'privacy-policy/', 
        TemplateView.as_view(template_name='privacy_policy.html'), 
        name='privacy_policy'
    ),
    path(
        'terms-of-service/', 
        TemplateView.as_view(template_name='terms_of_service.html'), 
        name='terms_of_service'
    ),
]
