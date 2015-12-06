# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0017_auto_20151205_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='instructor',
            field=models.CharField(default='', max_length=200, blank=True),
        ),
    ]
