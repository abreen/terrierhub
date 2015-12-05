# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0016_auto_20151205_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='building',
            field=models.ForeignKey(to='coursedb.Location', null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='room',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
