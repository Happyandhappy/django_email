# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_task_partial_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='from_date',
            field=models.DateField(default=datetime.date.today, null=True, verbose_name='From date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='to_date',
            field=models.DateField(default=datetime.date.today, null=True, verbose_name='To date', blank=True),
            preserve_default=True,
        ),
    ]
