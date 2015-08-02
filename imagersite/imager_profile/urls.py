from django.conf.urls import patterns, include, url

from .views import ImagerProfileDetailView


urlpatterns = patterns(
    '',
    url(r'^detail/(?P<pk>\d+)$', ImagerProfileDetailView.as_view(), name='detail'),
)

