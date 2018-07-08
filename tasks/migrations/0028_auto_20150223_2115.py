# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0027_auto_20150120_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='partial_paid_total',
            field=models.DecimalField(null=True, verbose_name='Partial paid total', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated at'),
            preserve_default=True,
        ),
    ]
