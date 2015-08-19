from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from braces.views import LoginRequiredMixin

from .models import Photo, Album


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
