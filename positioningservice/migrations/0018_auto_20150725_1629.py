# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import positioningservice.models


class Migration(migrations.Migration):

    dependencies = [
        ('positioningservice', '0017_auto_20150725_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffee',
            name='image',
            field=models.ImageField(max_length=2000, upload_to=positioningservice.models.content_file_name, default='media/pictures/no-image.jpg'),
        ),
    ]
