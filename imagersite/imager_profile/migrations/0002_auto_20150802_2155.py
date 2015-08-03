# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imager_profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagerprofile',
            name='address',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='camera',
            field=models.CharField(help_text='Enter your favorite camera.', max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='type_photography',
            field=models.CharField(help_text='What type of photgraphy do your prefer?', max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='imagerprofile',
            name='web_url',
            field=models.URLField(blank=True),
        ),
    ]
