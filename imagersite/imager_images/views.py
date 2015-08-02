#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
# from django.views.generic.base import TemplateView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.generic import ListView, DetailView
from imager_images.models import Photo, Album
from braces.views import LoginRequiredMixin


class LibraryView(LoginRequiredMixin, ListView):
    context_object_name = 'media'
    template_name = 'imager_images/library.html'

    def get_queryset(self):
        albums = get_list_or_404(Album, user=self.request.user)
        photos = get_list_or_404(Photo, user=self.request.user)
        return [albums, photos]


class AlbumView(LoginRequiredMixin, ListView):
    context_object_name = 'photos'
    template_name = 'imager_images/album.html'

    def get_queryset(self):
        album = get_object_or_404(Album, id=self.kwargs['pk'])
        return album.photos.all()


class PhotoView(LoginRequiredMixin, DetailView):
    model = Photo
    context_object_name = 'photo'
    template_name = 'imager_images/photo.html'
