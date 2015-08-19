#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django import template
from imager_images.models import Photo, Album
from django.db.models import Q


register = template.Library()


@register.filter
def authorized_albums(albums, user):
    return albums.filter(
        Q(user=user) | Q(published='shared') | Q(published='public')
    ).all()


@register.filter
def authorized_photos(photos, user):
    return photos.filter(
        Q(user=user) | Q(published='shared') | Q(published='public')
    ).all()


@register.filter
def album_is_authorized(album, user):
    return album.published in ['shared', 'public'] or album.user.id == user.id


@register.filter
def photo_is_authorized(photo, user):
    return photo.published in ['shared', 'public'] or photo.user.id == user.id


@register.filter
def album_is_editable(album, user):
    return album.published == 'public' or album.user.id == user.id


@register.filter
def photo_is_editable(photo, user):
    return photo.published == 'public' or photo.user.id == user.id


@register.filter
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})

