from __future__ import unicode_literals

import os

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import (ListView, CreateView, DetailView,
                                  UpdateView, TemplateView)
from django.http import HttpResponse
from braces.views import LoginRequiredMixin

from .models import Photo, Album, Face


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
    detect = False

    def get_queryset(self, *args, **kwargs):
        return super(PhotoView, self).get_queryset(*args, **kwargs).filter(
            Q(user=self.request.user) | Q(published='public')
        )

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        if self.detect and len(self.object.faces.all()) == 0:
            get_faces(self.object)

        context['faces'] = self.object.faces.all()
        return context


class AlbumAddView(LoginRequiredMixin, CreateView):
    template_name_suffix = '_add'
    model = Album
    fields = ['title', 'description', 'published', 'photos']
    success_url = '/images/library/'

    def get_form(self):
        form = super(AlbumAddView, self).get_form()
        form.fields['photos'].queryset = self.request.user.photos.all()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(AlbumAddView, self).form_valid(form)


class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    template_name_suffix = '_edit'
    model = Album
    fields = ['title', 'description', 'published', 'cover', 'photos']
    success_url = '/images/library/'

    def get_form(self):
        form = super(AlbumUpdateView, self).get_form()
        form.fields['photos'].queryset = self.request.user.photos.all()
        form.fields['cover'].queryset = form.instance.photos
        return form

    def get_object(self):
        obj = get_object_or_404(
            Album, user=self.request.user, pk=self.kwargs['pk']
        )
        return obj


class PhotoAddView(LoginRequiredMixin, CreateView):
    template_name_suffix = '_add'
    model = Photo
    fields = ['photo', 'title', 'description', 'published']
    success_url = '/images/library/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(PhotoAddView, self).form_valid(form)


class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    template_name_suffix = '_edit'
    model = Photo
    fields = ['photo', 'title', 'description', 'published']
    success_url = '/images/library'

    def get_object(self):
        obj = get_object_or_404(
            Photo, user=self.request.user, pk=self.kwargs['pk']
        )
        return obj


class FaceEditView(LoginRequiredMixin, TemplateView):
    model = Face

    def post(self, request, *args, **kwargs):
        try:
            face = Face.objects.get(id=request.POST['id'])
            face.name = request.POST['name']
            face.save()
        except (TypeError, Photo.DoesNotExist, Face.DoesNotExist):
            pass
        return HttpResponse()
