# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0039_auto_20151024_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentahead',
            name='from_date',
            field=models.DateField(default=datetime.date(2017, 6, 1), verbose_name='From date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateField(null=True, verbose_name='Month', blank=True),
            preserve_default=True,
        ),
    ]
