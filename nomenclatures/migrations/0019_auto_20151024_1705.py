# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0018_auto_20150223_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='priority',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tasktype',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
            preserve_default=True,
        ),
    ]
