from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Album, Photo


@receiver(post_delete, sender=User)
def delete_albums_for_user(sender, **kwargs):
    """Delete related albums when user is deleted."""
    instance = kwargs.get('instance')
    if not instance:
        return
    try:
        instance.albums.all().delete()
    except Album.DoesNotExist:
        pass


@receiver(post_delete, sender=User)
def delete_photos_for_user(sender, **kwargs):
    """Delete related photos when user is deleted."""
    instance = kwargs.get('instance')
    if not instance:
        return
    try:
        instance.photos.all().delete()
    except Photo.DoesNotExist:
        pass
