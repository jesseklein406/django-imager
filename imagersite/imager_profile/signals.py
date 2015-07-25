from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import ImagerProfile


@receiver(post_save, sender=User)
def create_profile_for_user(sender, **kwargs):
    """Add a related profile to user if needed."""
    instance = kwargs.get('instance')
    if not instance or kwargs.get('raw', False):
        return
    try:
        instance.profile
    except ImagerProfile.DoesNotExist:
        instance.profile = ImagerProfile()
        instance.profile.save()


@receiver(post_save, sender=ImagerProfile)
def create_user_for_profile(sender, **kwargs):
    """Add a related user to profile if needed."""
    instance = kwargs.get('instance')
    if not instance or kwargs.get('raw', False):
        return
    try:
        instance.user
    except User.UserDoesNotExist:
        instance.user = User()
        instance.user.save()


@receiver(post_delete, sender=User)
def delete_profile_for_user(sender, **kwargs):
    """Delete a related profile when user is deleted."""
    instance = kwargs.get('instance')
    if not instance:
        return
    try:
        instance.profile.delete()
    except ImagerProfile.DoesNotExist:
        pass


@receiver(post_delete, sender=ImagerProfile)
def delete_user_for_profile(sender, **kwargs):
    """Delete a related photos when user is deleted."""
    instance = kwargs.get('instance')
    if not instance:
        return
    try:
        instance.user.delete()
    except User.UserDoesNotExist:
        pass
