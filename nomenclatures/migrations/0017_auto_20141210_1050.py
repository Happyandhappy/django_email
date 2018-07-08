# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0016_auto_20141207_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktype',
            name='can_pay',
            field=models.BooleanField(default=False, help_text='Can pay description', verbose_name='Can pay'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tasktype',
            name='default_fee',
            field=models.BooleanField(default=False, help_text='Default fee description', verbose_name='Default fee'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tasktype',
            name='for_cachiers',
            field=models.BooleanField(default=False, help_text='For cachiers description', verbose_name='For cachiers'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tasktype',
            name='home_manager_fee',
            field=models.BooleanField(default=False, help_text='Home manager fee description', verbose_name='Home manager fee'),
            preserve_default=True,
        ),
    ]
