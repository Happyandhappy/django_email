# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_costs', '0012_auto_20141113_1636'),
        ('tasks', '0018_schedule'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'verbose_name': 'Schedule', 'verbose_name_plural': 'Schedules'},
        ),
        migrations.AddField(
            model_name='task',
            name='dynamic_cost',
            field=models.ForeignKey(blank=True, to='dynamic_costs.DynamicCost', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='apartment',
            field=smart_selects.db_fields.ChainedForeignKey(verbose_name='Apartment', blank=True, to='entrances.Apartment', null=True),
            preserve_default=True,
        ),
    ]
