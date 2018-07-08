# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entrances', '0037_auto_20151206_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntranceKasaSummary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'EntranceKasaSummary',
                'verbose_name_plural': 'EntranceKasaSummary',
            },
            bases=(models.Model,),
        ),
    ]
