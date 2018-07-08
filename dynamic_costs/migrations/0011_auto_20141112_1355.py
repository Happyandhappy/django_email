# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0006_auto_20141112_0944'),
        ('dynamic_costs', '0010_auto_20141112_1234'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamiccost',
            name='priority',
            field=select2.fields.ForeignKey(default=0, verbose_name='priority', to='nomenclatures.Priority'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dynamiccost',
            name='task_type',
            field=select2.fields.ForeignKey(default=0, verbose_name='task type', to='nomenclatures.TaskType'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='apartmentdynamiccost',
            name='apartment',
            field=models.ForeignKey(verbose_name='Apartment', to='entrances.Apartment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='apartmentdynamiccost',
            name='cost',
            field=models.ForeignKey(verbose_name='Apartment', to='dynamic_costs.DynamicCost'),
            preserve_default=True,
        ),
    ]
