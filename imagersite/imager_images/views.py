#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render
from imager_images.models import Photo, Album, Face
from braces.views import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import os


def get_faces(photo):
    import Algorithmia
    import base64
    Algorithmia.apiKey = os.environ['ALGORITHMIA_KEY']
    with open(photo.photo.path, "rb") as img:
        b64 = base64.b64encode(img.read())

    result = Algorithmia.algo("/ANaimi/FaceDetection").pipe(b64)

    faces = []
    for rect in result:
        face = Face()
        face.photo = photo
        face.name = '?'
        face.x = rect['x']
        face.y = rect['y']
        face.width = rect['width']
        face.height = rect['height']
        face.save()
        faces.append(face)

    return faces


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


@login_required
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
        for i in request.POST.getlist('photos'):
            album.photos.add(Photo.objects.get(id=int(i)))
        album.save()

        return HttpResponseRedirect(reverse('library'))

    else:
        return render(request, 'imager_images/album_add.html')


@login_required
def album_update(request, pk):
    album = Album.objects.get(id=pk)
    if request.POST and (
        request.user == album.user or album.published == 'public'
    ):
        album.title = request.POST['title']
        album.description = request.POST['description']
        album.published = request.POST['published']
        album.cover = Photo.objects.get(id=int(request.POST['cover']))
        album.photos.clear()
        for i in request.POST.getlist('photos'):
            album.photos.add(Photo.objects.get(id=int(i)))
        album.save()

        return HttpResponseRedirect(reverse('library'))

    else:
        return render(request, 'imager_images/album_edit.html', {'album': album})


@login_required
def photo_create(request):
    if request.POST:
        photo = Photo(
            user=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            published=request.POST['published'],
            photo=request.FILES['photo']
        )
        photo.save()

        return HttpResponseRedirect(reverse('library'))

    else:
        return render(request, 'imager_images/photo_add.html')


@login_required
def photo_update(request, pk):
    photo = Photo.objects.get(id=pk)
    if request.POST and (
        request.user == photo.user or photo.published == 'public'
    ):
        photo.title = request.POST['title']
        photo.description = request.POST['description']
        photo.published = request.POST['published']
        photo.save()

        return HttpResponseRedirect(reverse('library'))

    else:
        return render(request, 'imager_images/photo_edit.html', {'photo': photo})
