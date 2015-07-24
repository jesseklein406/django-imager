import six

from django.db import models
from django.contrib.auth.models import ActiveProfileManager, User


@six.python_2_unicode_compatible
class ImagerProfile(models.Model):
    user = models.OneToOneField(
        User,
        nullable=False
    )
    fav_camera = models.CharField(
        max_length=30
    )
    address = models.CharField()
    web_url = models.URLField()
    type_photography = models.CharField(max_length=30)

    objects = models.Manager()
    active = ActiveProfileManager()

    def __str__(self):
        return "{}'s profile".format(self.user.username)

    def is_active(self):
        return self.user.is_active
