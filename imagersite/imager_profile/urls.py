from django.conf.urls import patterns, url

from .views import ProfileDetailView, ProfileUpdateView


urlpatterns = patterns(
    '',
    url(r'^$', ProfileDetailView.as_view(), name='detail'),
    url(r'^edit/(?P<pk>\d+)', ProfileUpdateView.as_view(), name='edit')
)

