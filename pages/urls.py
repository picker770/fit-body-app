from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('features/', TemplateView.as_view(template_name='pages/features.html'), name='features'),
    path('pricing/', TemplateView.as_view(template_name='pages/pricing.html'), name='pricing'),
    path('contact/', views.contact, name='contact'),
]
