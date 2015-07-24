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
    file = models.ImageField(upload_to='photo_files/%Y-%m-%d')
    user = models.ForeignKey(
        User,
        null=False
    )
    title = models.CharField()
    description = models.TextField()
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField()
    published = models.CharField(
        maxlength=256,
        choices=PUBLISHED_CHOICES,
        default='private'
    )
  
