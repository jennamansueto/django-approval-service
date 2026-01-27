"""URL configuration for accounts app."""
from django.conf.urls import url

from .views import LoginView, LogoutView, MeView

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^me/$', MeView.as_view(), name='me'),
    url(r'^profile/$', MeView.as_view(), name='profile'),
    url(r'^user/current/$', MeView.as_view(), name='current-user'),
]
