from django.conf.urls import patterns, url

from .views import ProfileDetailView


urlpatterns = patterns(
    '',
    url(r'^detail/(?P<pk>\d+)$', ProfileDetailView.as_view(), name='detail'),
)

