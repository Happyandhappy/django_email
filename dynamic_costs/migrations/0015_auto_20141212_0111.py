# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_costs', '0014_auto_20141210_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccost',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, blank=True, help_text='For entire entrance', null=True, verbose_name='Price'),
            preserve_default=True,
        ),
    ]
