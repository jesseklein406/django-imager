from django.conf.urls import patterns, url

from .views import ProfileDetailView


urlpatterns = patterns(
    '',
    url(r'^$', ProfileDetailView.as_view(), name='detail'),
)

