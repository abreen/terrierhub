# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0013_auto_20151205_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='open_seats',
            field=models.IntegerField(null=True, verbose_name='open seats'),
        ),
    ]
