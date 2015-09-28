# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0002_department_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='school',
            field=models.ForeignKey(default=None, to='coursedb.School'),
            preserve_default=False,
        ),
    ]
