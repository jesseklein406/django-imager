from django.conf.urls import patterns, url

from .views import ProfileDetailView, profile_update_view


urlpatterns = patterns(
    '',
    url(r'^$', ProfileDetailView.as_view(), name='detail'),
    url(r'^edit/$', profile_update_view, name='edit')
)

