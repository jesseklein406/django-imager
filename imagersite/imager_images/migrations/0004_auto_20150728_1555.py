# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_images', '0003_auto_20150726_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date_published',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_published',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='title',
            field=models.CharField(max_length=256, blank=True),
        ),
    ]
