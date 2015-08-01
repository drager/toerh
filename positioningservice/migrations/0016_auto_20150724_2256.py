# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('positioningservice', '0015_coffee_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='position',
            name='longitude',
            field=models.FloatField(),
        ),
    ]
