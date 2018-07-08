# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0010_tasktype_for_entrance_only'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasktype',
            name='for_entrance_only',
        ),
        migrations.AddField(
            model_name='tasktype',
            name='from_cash_desk',
            field=models.BooleanField(default=False, help_text='paid from the entrances cash desk', verbose_name='from cash desk'),
            preserve_default=True,
        ),
    ]
