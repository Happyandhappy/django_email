# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_costs', '0012_auto_20141113_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamiccost',
            name='entrance',
            field=select2.fields.ForeignKey(verbose_name='Entrance', to='entrances.Entrance'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dynamiccost',
            name='priority',
            field=select2.fields.ForeignKey(verbose_name='Priority', to='nomenclatures.Priority'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dynamiccost',
            name='task_type',
            field=select2.fields.ForeignKey(verbose_name='Task type', to='nomenclatures.TaskType'),
            preserve_default=True,
        ),
    ]
