#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
# from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, render
from imager_images.models import Photo, Album
from braces.views import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class LibraryView(LoginRequiredMixin, ListView):
    context_object_name = 'media'
    template_name = 'imager_images/library.html'

    def get_queryset(self):
        albums = self.request.user.albums.all()
        photos = self.request.user.photos.all()
        return [albums, photos]


class AlbumView(LoginRequiredMixin, ListView):
    context_object_name = 'media'
    template_name = 'imager_images/album.html'

    def get_queryset(self):
        album = get_object_or_404(Album, id=self.kwargs['pk'])
        photos = album.photos.all()
        return [album, photos]


class PhotoView(LoginRequiredMixin, DetailView):
    model = Photo
    context_object_name = 'photo'
    template_name = 'imager_images/photo.html'


def album_create(request):
    if request.POST:
        album = Album(
            user=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            published=request.POST['published'],
            cover=Photo.objects.get(id=int(request.POST['cover']))
        )
        album.save()
        for i in request.POST['photos']:
            album.photos.add(Photo.objects.get(id=int(i)))
            album.save()

        return HttpResponseRedirect(reverse('library'))

    else:
        return render(request, 'imager_images/album_add.html')


class AlbumUpdate(LoginRequiredMixin, UpdateView):
    model = Album
    fields = ['name']


class PhotoCreate(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['name']


class PhotoUpdate(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['name']
