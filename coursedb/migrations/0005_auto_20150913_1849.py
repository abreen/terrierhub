# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0004_remove_course_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(verbose_name='course description', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='note',
            field=models.TextField(blank=True),
        ),
    ]
