# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0007_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='address',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
