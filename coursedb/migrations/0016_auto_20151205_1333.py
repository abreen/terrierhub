# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0015_auto_20151205_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='end_date',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meeting',
            name='start_date',
            field=models.DateField(default=datetime.date(2000, 1, 2)),
            preserve_default=False,
        ),
    ]
