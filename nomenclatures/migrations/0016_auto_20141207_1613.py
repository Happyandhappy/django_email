# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0015_tasktype_home_manager_fee'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='priority',
            options={'verbose_name': 'Priority', 'verbose_name_plural': 'Priorities'},
        ),
        migrations.AlterModelOptions(
            name='tasktype',
            options={'verbose_name': 'Task type', 'verbose_name_plural': 'Task types'},
        ),
        migrations.AlterField(
            model_name='tasktype',
            name='can_pay',
            field=models.BooleanField(default=False, verbose_name='Can payl'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tasktype',
            name='can_pay_partial',
            field=models.BooleanField(default=False, verbose_name='Can pay partial'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tasktype',
            name='for_cachiers',
            field=models.BooleanField(default=False, verbose_name='For cachiers'),
            preserve_default=True,
        ),
    ]
