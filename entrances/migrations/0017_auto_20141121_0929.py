# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import select2.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0012_remove_tasktype_from_cash_desk'),
        ('entrances', '0016_auto_20141121_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrance',
            name='monthly_expences',
            field=select2.fields.ManyToManyField(to='nomenclatures.TaskType', verbose_name='Monthly expences', through='entrances.MonthlyExpence'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monthlyexpence',
            name='entrance',
            field=models.ForeignKey(default='', verbose_name='entrance', to='entrances.Entrance'),
            preserve_default=False,
        ),
    ]
