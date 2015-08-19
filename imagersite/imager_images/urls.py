from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (
    LibraryView,
    PhotoAddView,
    PhotoView,
    AlbumView,
    AlbumAddView,
    AlbumUpdateView,
    PhotoUpdateView,
    FaceEditView
)


urlpatterns = patterns(
    '',
    url(r'^library/$', LibraryView.as_view(), name='library'),
    url(r'^album/(?P<pk>\d+)/$', AlbumView.as_view(), name='album'),
    url(r'^photos/(?P<pk>\d+)/$', PhotoView.as_view(), name='photo'),
    url(r'^album/add/$', AlbumAddView.as_view(), name='album_add'),
    url(
        r'^album/(?P<pk>\d+)/edit/$',
        AlbumUpdateView.as_view(),
        name='album_edit'
    ),
    url(r'^photos/add/$', PhotoAddView.as_view(), name='photo_add'),
    url(
        r'^photos/(?P<pk>\d+)/edit/$',
        PhotoUpdateView.as_view(),
        name='photo_edit'
    ),
    url(
        r'^photos/(?P<pk>\d+)/detect/$',
        PhotoView.as_view(detect=True),
        name='detect_faces'
    ),
    url(
        r'^photos/(?P<pk>\d+)/face/edit/$',
        FaceEditView.as_view(),
        name='edit_face'
    ),
)
