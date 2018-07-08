# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import vhodove.helper


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0033_auto_20150614_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='date',
            field=models.DateField(default=vhodove.helper.first_day_of_month, null=True, verbose_name='Month', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='from_date',
            field=models.DateField(default=vhodove.helper.first_day_of_month, verbose_name='From date', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='to_date',
            field=models.DateField(default=vhodove.helper.last_day_of_month, verbose_name='To date', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
