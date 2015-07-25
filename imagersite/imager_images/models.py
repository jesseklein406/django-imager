import six

from django.db import models
from django.contrib.auth.models import User


PUBLISHED_CHOICES = (
    ('private', 'private'),
    ('shared', 'shared'),
    ('public', 'public')
)


@six.python_2_unicode_compatible
class Photo(models.Model):
    user = models.ForeignKey(
        User,
        null=False
    )
    photo = models.ImageField(upload_to='photo_files/%Y-%m-%d')
    title = models.CharField(maxlength=256)
    description = models.TextField()
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField()
    published = models.CharField(
        maxlength=256,
        choices=PUBLISHED_CHOICES,
        default='private'
    )

    def __str__(self):
        return "Photo: {}".format(self.title)


@six.python_2_unicode_compatible
class Album(models.Model):
    user = models.ForeignKey(
        User,
        null=False
    )
    photos = models.ManyToManyField(
        Photo,
        related_name='album'
    )
    title = models.CharField(maxlength=256)
    description = models.TextField()
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField()
    published = models.CharField(
        maxlength=256,
        choices=PUBLISHED_CHOICES,
        default='private'
    )
    cover = models.ForeignKey(
        Photo,
        related_name='cover_photo'
    )

    def __str__(self):
        return "Album: {}".format(self.title)
