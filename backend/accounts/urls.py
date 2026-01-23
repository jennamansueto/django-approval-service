"""URL configuration for accounts app."""
from django.conf.urls import url

from .views import LoginView, LogoutView, MeView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^me/$', MeView.as_view(), name='me'),
]
