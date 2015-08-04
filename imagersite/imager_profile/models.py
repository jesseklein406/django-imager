from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class ActiveProfileManager(models.Manager):
    def get_queryset(self):
        return super(ActiveProfileManager, self).get_queryset().filter(
            user__is_active=True
        )


@python_2_unicode_compatible
class ImagerProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="profile",
        null=False
    )
    camera = models.CharField(
        max_length=256,
        help_text="Enter your favorite camera.",
        blank=True
    )
    address = models.CharField(max_length=256, blank=True)
    web_url = models.URLField(blank=True)
    type_photography = models.CharField(
        max_length=256,
        help_text="What type of photgraphy do your prefer?",
        blank=True
    )

    objects = models.Manager()
    active = ActiveProfileManager()

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def is_active(self):
        return self.user.is_active

    def get_absolute_url(self):
        return reverse('profile:detail')
