# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0014_auto_20151205_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='end',
            field=models.DateField(default=datetime.date(2001, 10, 10)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='section',
            name='start',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
            preserve_default=False,
        ),
    ]
