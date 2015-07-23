
from django.db import models
from django.contrib.auth.models import User
import six

@six.python_2_unicode_compatible
class ImagerProfile(models.Model):
    user = models.OneToOneField(User)
    fav_camera = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    web_url = models.URLField()
    type_photography = models.CharField(max_length=30)

