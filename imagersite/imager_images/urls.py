from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (
    LibraryView,
    PhotoView,
    AlbumView,
    album_create,
    album_update,
    photo_create,
    PhotoUpdateView
)


urlpatterns = patterns(
    '',
    url(r'^library/$', LibraryView.as_view(), name='library'),
    url(r'^album/(?P<pk>\d+)/$', AlbumView.as_view(), name='album'),
    url(r'^photos/(?P<pk>\d+)/$', PhotoView.as_view(), name='photo'),
    url(r'^album/add/$', album_create, name='album_add'),
    url(r'^album/(?P<pk>\d+)/edit/$', album_update, name='album_edit'),
    url(r'^photos/add/$', photo_create, name='photo_add'),
    url(
        r'^photos/(?P<pk>\d+)/edit/$',
        PhotoUpdateView.as_view(),
        name='photo_edit'
    ),
)
