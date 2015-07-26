# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(related_name='cover_photo', blank=True, to='imager_images.Photo', null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(related_name='photos', to=settings.AUTH_USER_MODEL),
        ),
    ]
