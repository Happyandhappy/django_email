# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_costs', '0012_auto_20141113_1636'),
        ('tasks', '0020_remove_task_dynamic_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='apartment_dynamic_cost',
            field=models.ForeignKey(blank=True, editable=False, to='dynamic_costs.ApartmentDynamicCost', null=True),
            preserve_default=True,
        ),
    ]
