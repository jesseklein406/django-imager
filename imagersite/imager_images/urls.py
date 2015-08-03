#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import patterns, url
from imager_images.views import (
    LibraryView,
    PhotoView,
    AlbumView,
    AlbumCreate,
    AlbumUpdate,
    PhotoCreate,
    PhotoUpdate
)


urlpatterns = patterns(
    '',
    url(r'^library/$', LibraryView.as_view(), name='library'),
    url(r'^album/(?P<pk>\d+)/$', AlbumView.as_view(), name='album'),
    url(r'^photos/(?P<pk>\d+)/$', PhotoView.as_view(), name='photo'),
    url(r'^album/add/$', AlbumCreate.as_view(), name='album_add'),
    url(r'^album/edit/(?P<pk>\d+)/$', AlbumUpdate.as_view(), name='album_edit'),
    url(r'^photos/add/$', PhotoCreate.as_view(), name='photo_add'),
    url(r'^photos/edit/(?P<pk>\d+)/$', PhotoUpdate.as_view(), name='photo_edit'),
)
