# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursedb', '0008_location_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('section', models.CharField(max_length=40)),
                ('open_seats', models.IntegerField(verbose_name='open seats')),
                ('instructor', models.CharField(max_length=200, verbose_name='instructor')),
                ('type', models.IntegerField(choices=[(0, 'applied art'), (1, 'discussion section'), (2, 'directed study'), (3, 'clinical experience'), (4, 'independent course'), (5, 'laboratory'), (6, 'lecture'), (7, 'other'), (8, 'pre-lab section')])),
                ('notes', models.CharField(max_length=600)),
                ('course', models.ForeignKey(to='coursedb.Course')),
            ],
        ),
    ]
