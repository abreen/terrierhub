# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0010_meeting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='notes',
            field=models.TextField(verbose_name='course description', blank=True),
        ),
    ]
