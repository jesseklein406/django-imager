#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import patterns, url
from imager_images.views import (
    LibraryView,
    PhotoView,
    AlbumView,
    album_create,
    album_update,
    photo_create,
    photo_update
)


urlpatterns = patterns(
    '',
    url(r'^library/$', LibraryView.as_view(), name='library'),
    url(r'^album/(?P<pk>\d+)/$', AlbumView.as_view(), name='album'),
    url(r'^photos/(?P<pk>\d+)/$', PhotoView.as_view(), name='photo'),
    url(r'^album/add/$', album_create, name='album_add'),
    url(r'^album/edit/(?P<pk>\d+)/$', album_update, name='album_edit'),
    url(r'^photos/add/$', photo_create, name='photo_add'),
    url(r'^photos/edit/(?P<pk>\d+)/$', photo_update, name='photo_edit'),
    url(r'^photos/(?P<pk>\d+)/face/edit/$', FaceEditView.as_view(), name='edit_face'),
)
