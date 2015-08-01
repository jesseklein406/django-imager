#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import patterns, url
from imager_images.views import LibraryView, PhotoView


urlpatterns = patterns(
    '',
    url(r'^library/$', LibraryView.as_view(), name='library'),
    # url(r'^album/(?P<pk>\d+)/$', AlbumView.as_view(), name='album'),
    url(r'^photo/(?P<pk>\d+)/$', PhotoView.as_view(), name='photo')
)
