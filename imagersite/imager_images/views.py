#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from imager_images.models import Photo, Album
from braces.views import LoginRequiredMixin


class LibraryView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'images/list.html'


class AlbumView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'images/list.html'


class PhotoView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'images/photo.html'
