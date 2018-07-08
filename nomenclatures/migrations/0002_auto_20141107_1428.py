# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktype',
            name='can_pay',
            field=models.BooleanField(default=False, verbose_name='can pay bill'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tasktype',
            name='can_pay_partial',
            field=models.BooleanField(default=False, verbose_name='can pay bill partial'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tasktype',
            name='for_cachiers',
            field=models.BooleanField(default=False, verbose_name='can cachier add this task type'),
            preserve_default=True,
        ),
    ]
