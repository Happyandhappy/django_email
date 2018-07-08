# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_auto_20141113_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='price_for_resolve',
            field=models.DecimalField(null=True, verbose_name='Price for resolve', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
