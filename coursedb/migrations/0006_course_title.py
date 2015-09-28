# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0005_auto_20150913_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='title',
            field=models.CharField(default=None, max_length=200, verbose_name='course title'),
            preserve_default=False,
        ),
    ]
