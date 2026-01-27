"""URL configuration for accounts app."""
from django.urls import re_path

from .views import LoginView, LogoutView, MeView

urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^me/$', MeView.as_view(), name='me'),
]
