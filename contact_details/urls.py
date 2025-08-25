from django.urls import path
from .views import ContactCreateView

urlpatterns = [
    path('contacts/', ContactCreateView.as_view(), name='contact-create'),
]