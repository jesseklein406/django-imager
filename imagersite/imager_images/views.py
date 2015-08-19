# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, UpdateView
from braces.views import LoginRequiredMixin

from imager_images.models import Photo, Album


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


class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    template_name_suffix = '_edit'
    model = Photo
    fields = ['title', 'description', 'published']
    success_url = '/images/library'
