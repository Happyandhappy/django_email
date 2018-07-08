# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0034_auto_20150809_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='from_date',
            field=models.DateField(verbose_name='From date', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='to_date',
            field=models.DateField(verbose_name='To date', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
