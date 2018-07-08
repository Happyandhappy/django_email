# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import vhodove.helper


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0036_merge'),
    ]

    operations = [
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
