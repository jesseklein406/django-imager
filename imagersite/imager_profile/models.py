import six

from django.db import models
from django.contrib.auth.models import User


class ActiveProfileManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProfileManager, self).get_queryset.filter(
            user__is_active=True
        )


@six.python_2_unicode_compatible
class ImagerProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="profile",
        null=False
    )
    fav_camera = models.CharField(
        max_length=30,
        help_text="Enter your favorite camera."
    )
    address = models.CharField()
    web_url = models.URLField()
    type_photography = models.CharField(
        max_length=30,
        help_text="What type of photgraphy do your prefer?"
    )

    objects = models.Manager()
    active = ActiveProfileManager()

    def __str__(self):
        return "{}'s profile".format(self.user.username)

    @property
    def is_active(self):
        return self.user.is_active
