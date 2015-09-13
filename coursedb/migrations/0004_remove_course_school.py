# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0003_department_school'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='school',
        ),
    ]
