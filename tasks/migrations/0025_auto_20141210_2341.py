# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import vhodove.helper


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0024_auto_20141210_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='from_date',
            field=models.DateField(default=vhodove.helper.first_day_of_month, verbose_name='From date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='to_date',
            field=models.DateField(default=vhodove.helper.last_day_of_month, verbose_name='To date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='from_date',
            field=models.DateField(default=vhodove.helper.first_day_of_month, null=True, verbose_name='From date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='to_date',
            field=models.DateField(default=vhodove.helper.last_day_of_month, null=True, verbose_name='To date', blank=True),
            preserve_default=True,
        ),
    ]
