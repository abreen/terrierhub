# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0012_auto_20151205_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='notes',
            field=models.CharField(blank=True, default='', max_length=600),
        ),
    ]
