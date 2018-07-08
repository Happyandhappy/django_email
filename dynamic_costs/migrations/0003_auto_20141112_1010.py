# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_costs', '0002_dynamiccost_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamiccost',
            name='price',
            field=models.DecimalField(null=True, verbose_name='Price', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dynamiccost',
            name='entrance',
            field=select2.fields.ForeignKey(verbose_name='entrance', to='entrances.Entrance'),
            preserve_default=True,
        ),
    ]
