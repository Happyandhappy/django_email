# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0015_task_price_for_resolve'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='resolved',
            field=models.BooleanField(default=False, verbose_name='Resolved'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='resolved_by_admin',
            field=models.BooleanField(default=False, verbose_name='Resolved by admin'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='price_for_resolve',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=8, blank=True, null=True, verbose_name='Price for resolve'),
            preserve_default=True,
        ),
    ]
