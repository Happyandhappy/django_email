# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import vhodove.helper


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_costs', '0013_auto_20141207_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccost',
            name='from_date',
            field=models.DateField(default=vhodove.helper.first_day_of_month, verbose_name='From date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dynamiccost',
            name='to_date',
            field=models.DateField(default=vhodove.helper.last_day_of_month, verbose_name='To date'),
            preserve_default=True,
        ),
    ]
