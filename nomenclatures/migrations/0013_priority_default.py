# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0012_remove_tasktype_from_cash_desk'),
    ]

    operations = [
        migrations.AddField(
            model_name='priority',
            name='default',
            field=models.BooleanField(default=False, verbose_name='Default'),
            preserve_default=True,
        ),
    ]
