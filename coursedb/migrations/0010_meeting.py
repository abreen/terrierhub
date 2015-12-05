# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0009_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('days', models.IntegerField()),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('room', models.CharField(max_length=40)),
                ('building', models.ForeignKey(to='coursedb.Location')),
                ('section', models.ForeignKey(to='coursedb.Section')),
            ],
        ),
    ]
