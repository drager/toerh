# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('positioningservice', '0016_auto_20150724_2256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coffee',
            name='position',
        ),
        migrations.AddField(
            model_name='coffee',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coffee',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
