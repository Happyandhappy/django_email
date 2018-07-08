# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_costs', '0011_auto_20141112_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccost',
            name='from_date',
            field=models.DateField(default=datetime.date.today, verbose_name='From date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dynamiccost',
            name='to_date',
            field=models.DateField(default=datetime.date.today, verbose_name='To date'),
            preserve_default=True,
        ),
    ]
