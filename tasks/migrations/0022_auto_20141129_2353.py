# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_costs', '0012_auto_20141113_1636'),
        ('tasks', '0021_task_apartment_dynamic_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='dynamic_cost',
            field=models.ForeignKey(blank=True, editable=False, to='dynamic_costs.DynamicCost', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='common_information',
            field=models.TextField(null=True, verbose_name='Common information', blank=True),
            preserve_default=True,
        ),
    ]
