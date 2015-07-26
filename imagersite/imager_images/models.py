from __future__ import unicode_literals
import os

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from imager_profile.models import ImagerProfile


PUBLISHED_CHOICES = (
    ('private', 'private'),
    ('shared', 'shared'),
    ('public', 'public')
)


@python_2_unicode_compatible
class Photo(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        related_name='photos'
    )
    photo = models.ImageField(upload_to='photo_files/%Y-%m-%d')
    title = models.CharField(max_length=256)
    description = models.TextField()
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(null=True)
    published = models.CharField(
        max_length=256,
        choices=PUBLISHED_CHOICES,
        default='private'
    )

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Album(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        related_name='albums'
    )
    photos = models.ManyToManyField(
        Photo,
        related_name='albums'
    )
    title = models.CharField(max_length=256)
    description = models.TextField()
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(null=True)
    published = models.CharField(
        max_length=256,
        choices=PUBLISHED_CHOICES,
        default='private'
    )
    cover = models.ForeignKey(
        Photo,
        related_name='+',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title
